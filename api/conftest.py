"""
Shared fixtures for API tests. Uses Google ID token as Bearer auth.
"""

import uuid
import pytest
import requests
from faker import Faker

from config import (
    API_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN,
    GOOGLE_TOKEN_URL,
)

fake = Faker()


@pytest.fixture(scope="session")
def api_url() -> str:
    return API_URL


@pytest.fixture(scope="session")
def google_id_token() -> str:
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
def auth_headers(google_id_token: str) -> dict:
    return {"Authorization": f"Bearer {google_id_token}"}


@pytest.fixture
def client_id(api_url: str, auth_headers: dict) -> str:
    resp = requests.post(
        f"{api_url}/clients",
        json={
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "email": fake.email(),
            "phoneNumber": fake.numerify("+1-###-###-####"),
        },
        headers=auth_headers,
    )
    resp.raise_for_status()
    return resp.json()


@pytest.fixture
def exercise_id(api_url: str, auth_headers: dict) -> str:
    resp = requests.post(
        f"{api_url}/exercises",
        json={"name": fake.word(), "type": "SET"},
        headers=auth_headers,
    )
    resp.raise_for_status()
    return resp.json()


@pytest.fixture
def workout_id(api_url: str, auth_headers: dict, client_id: str) -> str:
    resp = requests.post(
        f"{api_url}/clients/{client_id}/workouts",
        json={
            "workoutDate": fake.date_this_year().isoformat(),
            "workoutName": fake.catch_phrase(),
        },
        headers=auth_headers,
    )
    resp.raise_for_status()
    return resp.json()


@pytest.fixture
def workout_exercise_id(
    api_url: str, auth_headers: dict, client_id: str, workout_id: str, exercise_id: str
) -> str:
    resp = requests.post(
        f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises",
        json={"exerciseId": exercise_id},
        headers=auth_headers,
    )
    resp.raise_for_status()
    return resp.json()
