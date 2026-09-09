from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["ok"] is True


def test_portal():
    res = client.get("/")
    assert res.status_code == 200
    assert b"BELENTANI" in res.content


def test_judas():
    res = client.get("/judas")
    assert res.status_code == 200
    assert b"JUDAS" in res.content
