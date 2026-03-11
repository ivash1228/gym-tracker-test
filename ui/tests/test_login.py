"""
Login page tests — no authentication required.

These validate the login screen itself: does it render, does the
Google button work, is the page accessible.
"""

import re

from playwright.sync_api import Page, expect

from ui.pages.login_page import LoginPage


class TestLoginPage:

    def test_login_page_loads(self, page: Page):
        login = LoginPage(page)
        login.open()
        expect(login.heading).to_be_visible()
        expect(login.google_login_button).to_be_visible()

    def test_google_login_button_is_enabled(self, page: Page):
        login = LoginPage(page)
        login.open()
        expect(login.google_login_button).to_be_visible()
        expect(login.google_login_button).to_be_enabled()

    def test_google_login_opens_popup(self, page: Page):
        """Clicking the Google button should open a Google sign-in popup."""
        login = LoginPage(page)
        login.open()
        with page.expect_popup() as popup_info:
            login.click_google_login()
        popup = popup_info.value
        expect(popup).to_have_url(re.compile(r"accounts\.google\.com"))
        popup.close()

    def test_page_title_contains_app_name(self, page: Page):
        login = LoginPage(page)
        login.open()
        expect(page).to_have_title("Gym Tracker")

    def test_unauthenticated_user_sees_login(self, page: Page):
        """Navigating to a protected route without auth should show the login screen."""
        page.goto("/clients")
        login = LoginPage(page)
        expect(login.google_login_button).to_be_visible()
