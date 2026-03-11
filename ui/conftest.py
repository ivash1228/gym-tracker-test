import os
import pytest
import requests
from pathlib import Path
from playwright.sync_api import Page, BrowserContext, Playwright

from config import (
    BASE_URL, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN, GOOGLE_TOKEN_URL,
)

RESULTS_DIR = Path(__file__).parent / "test_results"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def google_id_token() -> str:
    """Exchange refresh token for a fresh Google ID token via API call."""
    response = requests.post(GOOGLE_TOKEN_URL, data={
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "refresh_token": GOOGLE_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    })
    response.raise_for_status()
    token = response.json().get("id_token")
    assert token, "Google did not return an id_token"
    return token


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    headless = os.getenv("HEADED", "false").lower() != "true"
    browser = playwright.chromium.launch(headless=headless)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser, base_url) -> BrowserContext:
    ctx = browser.new_context(base_url=base_url)
    ctx.set_default_timeout(15_000)
    yield ctx
    ctx.close()


@pytest.fixture()
def page(context) -> Page:
    pg = context.new_page()
    yield pg
    pg.close()


@pytest.fixture()
def auth_page(browser, base_url, google_id_token) -> Page:
    """Page pre-authenticated by injecting id_token into localStorage."""
    ctx = browser.new_context(base_url=base_url)
    ctx.set_default_timeout(15_000)
    pg = ctx.new_page()
    pg.goto("/")
    pg.evaluate(f"() => localStorage.setItem('idToken', '{google_id_token}')")
    pg.reload()
    yield pg
    pg.close()
    ctx.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Auto-capture a screenshot when any test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("auth_page") or item.funcargs.get("page")
        if page and not page.is_closed():
            RESULTS_DIR.mkdir(parents=True, exist_ok=True)
            path = RESULTS_DIR / f"{item.name}.png"
            page.screenshot(path=str(path), full_page=True)
