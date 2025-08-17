from fastapi.testclient import TestClient
from main import app  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""

# TODO Add more tests
def test_basic_mutiplication():
    r = client.post("/calculate", params={"expr": "8*9"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["result"] == 72

def test_mutiplication_on_percent():
    r = client.post("/calculate", params={"expr": "8*9%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.72) < 1e-9

def test_mutiplication_on_percent_with_basic_addition():
    r = client.post("/calculate", params={"expr": "20*3%+2"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 2.6) < 1e-9

def test_mutiplication_on_percent_with_basic_subtraction():
    r = client.post("/calculate", params={"expr": "30-4*10%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 29.6) < 1e-9