"""Add Client tests — requires authentication."""

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from ui.pages.client_page import ClientPage

fake = Faker()


class TestAddClient:

    def test_add_new_client_success(self, auth_page: Page):
        clients = ClientPage(auth_page)
        clients.open()
        clients.click_add_client()
        clients.fill_client_form(fake.first_name(), fake.last_name(), fake.email(), fake.numerify("+1-###-###-####"))
        clients.submit_form()
        expect(clients.success_toast).to_be_visible()

    def test_new_client_appears_in_list(self, auth_page: Page):
        clients = ClientPage(auth_page)
        clients.open()

        initial_count = clients.get_client_count()
        first_name = fake.first_name()

        clients.click_add_client()
        clients.fill_client_form(first_name, fake.last_name(), fake.email(), fake.numerify("+1-###-###-####"))
        clients.submit_form()

        expect(clients.success_toast).to_be_visible()
        expect(auth_page.get_by_text(first_name).first).to_be_visible()
        assert clients.get_client_count() == initial_count + 1

    def test_add_client_form_cancel(self, auth_page: Page):
        clients = ClientPage(auth_page)
        clients.open()

        initial_count = clients.get_client_count()

        clients.click_add_client()
        clients.fill_client_form(fake.first_name(), fake.last_name(), fake.email(), fake.numerify("+1-###-###-####"))
        clients.cancel_button.click()

        assert clients.get_client_count() == initial_count

    @pytest.mark.parametrize("first_name, last_name, email, phone, expected_error", [
        ("Jane", "Doe", "not-an-email", "+1-222-333-4444", "must be a well-formed email address"),
        ("Jane", "Doe", "", "+1-222-333-4444", "required"),
        ("", "Doe", "valid@test.com", "+1-222-333-4444", "First name is required"),
        ("Jane", "", "valid@test.com", "+1-222-333-4444", "Last name is required"),
    ])
    def test_add_client_validation(self, auth_page: Page, first_name, last_name, email, phone, expected_error):
        clients = ClientPage(auth_page)
        clients.open()
        clients.click_add_client()
        clients.fill_client_form(first_name, last_name, email, phone)
        clients.submit_form()
        expect(auth_page.get_by_text(expected_error, exact=False)).to_be_visible()
