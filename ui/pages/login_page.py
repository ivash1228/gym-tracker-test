"""
Page object for the Login / Landing screen.
"""

from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Gym Tracker")
        self.google_login_button = page.get_by_role("button", name="Sign in with Google")
        self.logo = page.locator("img[alt*='logo' i]")

    def open(self):
        self.navigate(self.PATH)
        return self

    def click_google_login(self):
        self.google_login_button.click()
