"""Authentication helpers shared by API/UI tests."""

from __future__ import annotations

import requests

from config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REFRESH_TOKEN,
    GOOGLE_TOKEN_URL,
)


def get_google_id_token() -> str:
    """Exchange refresh token for a fresh Google ID token."""
    response = requests.post(
        GOOGLE_TOKEN_URL,
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "refresh_token": GOOGLE_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )
    response.raise_for_status()
    token = response.json().get("id_token")
    assert token, "Google did not return an id_token"
    return token
