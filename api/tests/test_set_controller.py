"""API tests for set-controller. Auto-generated from OpenAPI spec."""

import uuid
import requests
from faker import Faker

fake = Faker()


def test_addSetToWorkout_success(api_url, auth_headers, client_id, workout_id, workout_exercise_id):
    """Happy path: POST /clients/{clientId}/workouts/{workoutId}/exercises/{workoutExerciseId}/sets returns 200."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises/{workout_exercise_id}/sets"
    body = {
        "weights": 10,
        "reps": 5,
    }
    
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 200


def test_addSetToWorkout_unauthorized(api_url, client_id, workout_id, workout_exercise_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises/{workout_exercise_id}/sets"
    body = {
        "weights": 10,
        "reps": 5,
    }
    
    resp = requests.post(url, json=body)
    assert resp.status_code == 401



def test_addSetToWorkout_missing_weights(api_url, auth_headers, client_id, workout_id, workout_exercise_id):
    """Missing required field weights returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises/{workout_exercise_id}/sets"
    body = {
        "reps": 5,
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_addSetToWorkout_invalid_weights(api_url, auth_headers, client_id, workout_id, workout_exercise_id):
    """Invalid weights (pattern/enum/format) returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises/{workout_exercise_id}/sets"
    body = {
        "weights": "not-a-number",
        "reps": 5,
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_addSetToWorkout_missing_reps(api_url, auth_headers, client_id, workout_id, workout_exercise_id):
    """Missing required field reps returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises/{workout_exercise_id}/sets"
    body = {
        "weights": 10,
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_addSetToWorkout_invalid_reps(api_url, auth_headers, client_id, workout_id, workout_exercise_id):
    """Invalid reps (pattern/enum/format) returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises/{workout_exercise_id}/sets"
    body = {
        "weights": 10,
        "reps": "not-a-number",
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400