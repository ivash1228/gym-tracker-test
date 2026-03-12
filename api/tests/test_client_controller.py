"""API tests for client-controller. Auto-generated from OpenAPI spec."""

import uuid
import requests
from faker import Faker

fake = Faker()


def test_updateClientEmail_success(api_url, auth_headers, client_id):
    """Happy path: PUT /clients/{clientId}/email returns 200."""
    url = f"{api_url}/clients/{client_id}/email"
    body = {
        "email": fake.email(),
    }
    
    resp = requests.put(url, headers=auth_headers, json=body)
    assert resp.status_code == 200


def test_updateClientEmail_unauthorized(api_url, client_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/email"
    body = {
        "email": fake.email(),
    }
    
    resp = requests.put(url, json=body)
    assert resp.status_code == 401



def test_updateClientEmail_missing_email(api_url, auth_headers, client_id):
    """Missing required field email returns 400."""
    url = f"{api_url}/clients/{client_id}/email"
    body = {

    }
    resp = requests.put(url, headers=auth_headers, json=body)
    assert resp.status_code == 400



def test_getClients_success(api_url, auth_headers):
    """Happy path: GET /clients returns 200."""
    url = f"{api_url}/clients"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getClients_unauthorized(api_url):
    """No auth header returns 401."""
    url = f"{api_url}/clients"
    resp = requests.get(url)
    assert resp.status_code == 401



def test_createClient_success(api_url, auth_headers):
    """Happy path: POST /clients returns 201."""
    url = f"{api_url}/clients"
    body = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####"),
    }
    
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 201


def test_createClient_unauthorized(api_url):
    """No auth header returns 401."""
    url = f"{api_url}/clients"
    body = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####"),
    }
    
    resp = requests.post(url, json=body)
    assert resp.status_code == 401



def test_createClient_missing_firstName(api_url, auth_headers):
    """Missing required field firstName returns 400."""
    url = f"{api_url}/clients"
    body = {
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####"),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400



def test_createClient_missing_lastName(api_url, auth_headers):
    """Missing required field lastName returns 400."""
    url = f"{api_url}/clients"
    body = {
        "firstName": fake.first_name(),
        "email": fake.email(),
        "phoneNumber": fake.numerify("+1-###-###-####"),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400



def test_createClient_missing_email(api_url, auth_headers):
    """Missing required field email returns 400."""
    url = f"{api_url}/clients"
    body = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "phoneNumber": fake.numerify("+1-###-###-####"),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400



def test_createClient_missing_phoneNumber(api_url, auth_headers):
    """Missing required field phoneNumber returns 400."""
    url = f"{api_url}/clients"
    body = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_createClient_invalid_phoneNumber(api_url, auth_headers):
    """Invalid phoneNumber (pattern/enum/format) returns 400."""
    url = f"{api_url}/clients"
    body = {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "phoneNumber": 'invalid',
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_getClientByID_success(api_url, auth_headers, client_id):
    """Happy path: GET /clients/{clientId} returns 200."""
    url = f"{api_url}/clients/{client_id}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getClientByID_unauthorized(api_url, client_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}"
    resp = requests.get(url)
    assert resp.status_code == 401


def test_getClientByID_not_found(api_url, auth_headers):
    """Non-existent ID returns 404."""
    url = f"{api_url}/clients/{str(uuid.uuid4())}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 404