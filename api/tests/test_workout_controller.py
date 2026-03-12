"""API tests for workout-controller. Auto-generated from OpenAPI spec."""

import uuid
import requests
from faker import Faker

fake = Faker()


def test_getAllWorkoutsForClient_success(api_url, auth_headers, client_id):
    """Happy path: GET /clients/{clientId}/workouts returns 200."""
    url = f"{api_url}/clients/{client_id}/workouts"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getAllWorkoutsForClient_unauthorized(api_url, client_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/workouts"
    resp = requests.get(url)
    assert resp.status_code == 401


def test_getAllWorkoutsForClient_not_found(api_url, auth_headers):
    """Non-existent ID returns 404."""
    url = f"{api_url}/clients/{str(uuid.uuid4())}/workouts"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 404


def test_addWorkout_success(api_url, auth_headers, client_id):
    """Happy path: POST /clients/{clientId}/workouts returns 200."""
    url = f"{api_url}/clients/{client_id}/workouts"
    body = {
        "workoutDate": fake.date_this_year().isoformat(),
        "workoutName": fake.catch_phrase()[:30],
    }
    
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 200


def test_addWorkout_unauthorized(api_url, client_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/workouts"
    body = {
        "workoutDate": fake.date_this_year().isoformat(),
        "workoutName": fake.catch_phrase()[:30],
    }
    
    resp = requests.post(url, json=body)
    assert resp.status_code == 401



def test_addWorkout_missing_workoutDate(api_url, auth_headers, client_id):
    """Missing required field workoutDate returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts"
    body = {
        "workoutName": fake.catch_phrase()[:30],
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_addWorkout_invalid_workoutDate(api_url, auth_headers, client_id):
    """Invalid workoutDate (pattern/enum/format) returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts"
    body = {
        "workoutDate": '2025-13-99',
        "workoutName": fake.catch_phrase(),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_addWorkout_missing_workoutName(api_url, auth_headers, client_id):
    """Missing required field workoutName returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts"
    body = {
        "workoutDate": fake.date_this_year().isoformat(),
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400



def test_getFullWorkout_success(api_url, auth_headers, client_id, workout_id):
    """Happy path: GET /clients/{clientId}/workouts/{workoutId} returns 200."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getFullWorkout_unauthorized(api_url, client_id, workout_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}"
    resp = requests.get(url)
    assert resp.status_code == 401


def test_getFullWorkout_not_found(api_url, auth_headers):
    """Non-existent ID returns 404."""
    url = f"{api_url}/clients/{str(uuid.uuid4())}/workouts/{str(uuid.uuid4())}"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 404