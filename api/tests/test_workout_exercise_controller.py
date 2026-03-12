"""API tests for workout-exercise-controller. Auto-generated from OpenAPI spec."""

import uuid
import requests
from faker import Faker

fake = Faker()


def test_getWorkoutExercises_success(api_url, auth_headers, client_id, workout_id):
    """Happy path: GET /clients/{clientId}/workouts/{workoutId}/exercises returns 200."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 200


def test_getWorkoutExercises_unauthorized(api_url, client_id, workout_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises"
    resp = requests.get(url)
    assert resp.status_code == 401


def test_getWorkoutExercises_not_found(api_url, auth_headers):
    """Non-existent ID returns 404."""
    url = f"{api_url}/clients/{str(uuid.uuid4())}/workouts/{str(uuid.uuid4())}/exercises"
    resp = requests.get(url, headers=auth_headers)
    assert resp.status_code == 404


def test_addExerciseToWorkout_success(api_url, auth_headers, client_id, workout_id, exercise_id):
    """Happy path: POST /clients/{clientId}/workouts/{workoutId}/exercises returns 200."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises"
    body = {
        "exerciseId": exercise_id,
    }
    
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 200


def test_addExerciseToWorkout_unauthorized(api_url, client_id, workout_id, exercise_id):
    """No auth header returns 401."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises"
    body = {
        "exerciseId": exercise_id,
    }
    
    resp = requests.post(url, json=body)
    assert resp.status_code == 401



def test_addExerciseToWorkout_missing_exerciseId(api_url, auth_headers, client_id, workout_id, exercise_id):
    """Missing required field exerciseId returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises"
    body = {

    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400


def test_addExerciseToWorkout_invalid_exerciseId(api_url, auth_headers, client_id, workout_id, exercise_id):
    """Invalid exerciseId (pattern/enum/format) returns 400."""
    url = f"{api_url}/clients/{client_id}/workouts/{workout_id}/exercises"
    body = {
        "exerciseId": 'not-a-uuid',
    }
    resp = requests.post(url, headers=auth_headers, json=body)
    assert resp.status_code == 400