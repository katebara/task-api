def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_list_tasks_empty(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_create_task(client):
    resp = client.post("/tasks", json={"title": "Write CI pipeline doc"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Write CI pipeline doc"
    assert body["done"] is False
    assert "id" in body


def test_create_task_missing_title(client):
    resp = client.post("/tasks", json={})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_create_task_bad_title_type(client):
    resp = client.post("/tasks", json={"title": 12345})
    assert resp.status_code == 400


def test_get_task(client):
    created = client.post("/tasks", json={"title": "Set up GitHub Actions"}).get_json()
    resp = client.get(f"/tasks/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Set up GitHub Actions"


def test_get_task_not_found(client):
    resp = client.get("/tasks/999")
    assert resp.status_code == 404


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Draft"}).get_json()
    resp = client.put(f"/tasks/{created['id']}", json={"done": True})
    assert resp.status_code == 200
    assert resp.get_json()["done"] is True


def test_update_task_bad_title(client):
    created = client.post("/tasks", json={"title": "Draft"}).get_json()
    resp = client.put(f"/tasks/{created['id']}", json={"title": ""})
    assert resp.status_code == 400


def test_update_task_not_found(client):
    resp = client.put("/tasks/999", json={"done": True})
    assert resp.status_code == 404


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Temp"}).get_json()
    resp = client.delete(f"/tasks/{created['id']}")
    assert resp.status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found(client):
    resp = client.delete("/tasks/999")
    assert resp.status_code == 404


def test_list_tasks_after_create(client):
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    resp = client.get("/tasks")
    assert len(resp.get_json()) == 2
