"""
Shared fixtures for API tests. Uses Google ID token as Bearer auth.
"""

import pytest
import requests
from faker import Faker

from config import (
    API_URL,
)
from utils.auth import get_google_id_token

fake = Faker()


def raise_with_details(resp: requests.Response, context: str) -> str:
    """Raise AssertionError with response body details for fixture setup failures."""
    if resp.status_code >= 400:
        raise AssertionError(
            f"{context} failed with {resp.status_code}\n"
            f"Response: {resp.text}"
        )
    return resp.json()


@pytest.fixture(scope="session")
def api_url() -> str:
    return API_URL


@pytest.fixture(scope="session")
def google_id_token() -> str:
    return get_google_id_token()


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
    return raise_with_details(resp, "POST /clients")


@pytest.fixture
def exercise_id(api_url: str, auth_headers: dict) -> str:
    resp = requests.post(
        f"{api_url}/exercises",
        json={"name": fake.word(), "type": "SET"},
        headers=auth_headers,
    )
    return raise_with_details(resp, "POST /exercises")


@pytest.fixture
def workout_id(api_url: str, auth_headers: dict, client_id: str) -> str:
    resp = requests.post(
        f"{api_url}/clients/{client_id}/workouts",
        json={
            "workoutDate": fake.date_this_year().isoformat(),
            "workoutName": fake.catch_phrase()[:30],
        },
        headers=auth_headers,
    )
    return raise_with_details(resp, "POST /clients/{clientId}/workouts")


@pytest.fixture
def workout_exercise_id(
    api_url: str, auth_headers: dict, client_id: str, workout_id: str, exercise_id: str
) -> str:
    resp = requests.post(
        f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises",
        json={"exerciseId": exercise_id},
        headers=auth_headers,
    )
    return raise_with_details(resp, "POST /clients/{clientId}/workouts/{workoutId}/exercises")
