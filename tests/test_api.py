from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_metrics_flow():
    r = client.post("/metrics", json={"device_id": "dev-1", "temperature": 22.5})
    assert r.status_code == 200
    body = r.json()
    assert body["device_id"] == "dev-1"
    assert body["temperature"] == 22.5
    assert "ts" in body

    r2 = client.get("/metrics?limit=5")
    assert r2.status_code == 200
    items = r2.json()
    assert len(items) >= 1
