import requests

BASE = "https://api.test.fiindo.com/api/v1"
TOKEN = "fionn.zak"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_healthcheck():
    resp = requests.get("https://api.test.fiindo.com/health", headers=HEADERS)
    assert resp.status_code == 200
    assert "Ok" in resp.text

def test_symbols_endpoint():
    resp = requests.get(f"{BASE}/symbols", headers=HEADERS)
    assert resp.status_code == 200

    data = resp.json()
    assert "symbols" in data
    assert isinstance(data["symbols"], list)
    assert len(data["symbols"]) > 0
