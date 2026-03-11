"""Page object for the Client management screen."""

from playwright.sync_api import Page
from ui.pages.base_page import BasePage


class ClientPage(BasePage):
    PATH = "/clients"

    def __init__(self, page: Page):
        super().__init__(page)
        # Locators
        self.add_client_button = page.get_by_role("button", name="Add New Client")
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.email_input = page.get_by_placeholder("Email")
        self.phone_input = page.get_by_placeholder("Phone Number")
        self.save_button = page.get_by_role("button", name="Create Client")
        self.cancel_button = page.get_by_role("button", name="Cancel")
        self.success_toast = page.get_by_role("alert").filter(has_text="Client created successfully")
        self.error_toast = page.get_by_role("alert")
        self.client_items = page.locator("button.button.success")

    def open(self):
        self.navigate(self.PATH)
        self.add_client_button.wait_for(state="visible")
        return self

    def click_add_client(self):
        self.add_client_button.click()

    def fill_client_form(self, first_name: str, last_name: str, email: str, phone: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)

    def submit_form(self):
        self.save_button.click()

    def get_client_count(self) -> int:
        return self.client_items.count()
