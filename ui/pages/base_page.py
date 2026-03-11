from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "/"):
        self.page.goto(path)

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_url(self, url_pattern: str, timeout: int = 10_000):
        self.page.wait_for_url(url_pattern, timeout=timeout)
