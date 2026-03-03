"""Simple smoke test - app is reachable."""
import httpx

BASE_URL = "http://localhost:3000"
API_URL = "http://localhost:8080"


def test_frontend_loads():
    r = httpx.get(f"{BASE_URL}/", follow_redirects=True)
    assert r.status_code == 200
    assert "Gym Tracker" in r.text or "gym" in r.text.lower()


def test_backend_health():
    r = httpx.get(f"{API_URL}/actuator/health")
    assert r.status_code == 200