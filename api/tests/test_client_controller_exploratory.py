"""Exploratory tests for POST /clients. LLM-generated."""

import pytest
import requests
from faker import Faker

fake = Faker()


def test_post_clients_firstname_as_number(api_url, auth_headers):
    """Type mismatch: firstName as number instead of string"""
    body = {
        "firstName": 12345,
        "lastName": "Smith",
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####")
    }
    resp = requests.post(f"{api_url}/clients", headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_post_clients_lastname_null(api_url, auth_headers):
    """Null value for required lastName field"""
    body = {
        "firstName": "John",
        "lastName": None,
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####")
    }
    resp = requests.post(f"{api_url}/clients", headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_post_clients_email_empty_string(api_url, auth_headers):
    """Empty string for required email field"""
    body = {
        "firstName": "John",
        "lastName": "Smith",
        "email": "",
        "phoneNumber": fake.numerify("+1-###-###-####")
    }
    resp = requests.post(f"{api_url}/clients", headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_post_clients_phonenumber_invalid_format(api_url, auth_headers):
    """phoneNumber as wrong format (invalid pattern)"""
    body = {
        "firstName": "John",
        "lastName": "Smith",
        "email": fake.email(),
        "phoneNumber": "555-1234"
    }
    resp = requests.post(f"{api_url}/clients", headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_post_clients_extra_unknown_field(api_url, auth_headers):
    """Extra unknown field in payload"""
    body = {
        "firstName": "John",
        "lastName": "Smith",
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####"),
        "unknownField": "some_value"
    }
    resp = requests.post(f"{api_url}/clients", headers=auth_headers, json=body)
    assert resp.status_code in (200, 201, 400, 422)