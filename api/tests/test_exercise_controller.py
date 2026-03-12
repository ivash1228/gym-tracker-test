"""API tests for exercise-controller. Auto-generated from OpenAPI spec."""

import uuid
import requests
from faker import Faker

fake = Faker()


def test_getAllExercises_success(api_url, auth_headers):
    """Happy path: GET /exercises returns 200."""
    url = f"{api_url}/exercises"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getAllExercises_unauthorized(api_url):
    """No auth header returns 401."""
    url = f"{api_url}/exercises"
    resp = requests.get(url)
    assert resp.status_code == 401



def test_createExercise_success(api_url, auth_headers):
    """Happy path: POST /exercises returns 200."""
    url = f"{api_url}/exercises"
    body = {
        "name": fake.word(),
        "type": 'SET',
    }
    
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 200


def test_createExercise_unauthorized(api_url):
    """No auth header returns 401."""
    url = f"{api_url}/exercises"
    body = {
        "name": fake.word(),
        "type": 'SET',
    }
    
    resp = requests.post(url, json=body)
    assert resp.status_code == 401



def test_createExercise_missing_name(api_url, auth_headers):
    """Missing required field name returns 400."""
    url = f"{api_url}/exercises"
    body = {
        "type": 'SET',
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400



def test_createExercise_missing_type(api_url, auth_headers):
    """Missing required field type returns 400."""
    url = f"{api_url}/exercises"
    body = {
        "name": fake.word(),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_createExercise_invalid_type(api_url, auth_headers):
    """Invalid type (pattern/enum/format) returns 400."""
    url = f"{api_url}/exercises"
    body = {
        "name": fake.word(),
        "type": 'INVALID_ENUM',
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_getExerciseById_success(api_url, auth_headers, exercise_id):
    """Happy path: GET /exercises/{exerciseId} returns 200."""
    url = f"{api_url}/exercises/{exercise_id}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getExerciseById_unauthorized(api_url, exercise_id):
    """No auth header returns 401."""
    url = f"{api_url}/exercises/{exercise_id}"
    resp = requests.get(url)
    assert resp.status_code == 401


def test_getExerciseById_not_found(api_url, auth_headers):
    """Non-existent ID returns 404."""
    url = f"{api_url}/exercises/{str(uuid.uuid4())}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 404