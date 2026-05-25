from pathlib import Path
import sys

import pytest

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROBLEM_ROOT / "src"))

from task_api import InMemoryTaskStore, create_app


def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def post_json(test_client, path, payload):
    return test_client.post(path, json=payload)


def test_create_app_returns_testable_app():
    app = create_app()
    assert hasattr(app, "test_client")


def test_health_route_returns_ok():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_project_returns_201():
    response = post_json(client(), "/projects", {"name": "Platform"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Platform"


def test_create_project_trims_name():
    response = post_json(client(), "/projects", {"name": "  Platform  "})
    assert response.get_json()["name"] == "Platform"


def test_create_project_rejects_blank_name():
    response = post_json(client(), "/projects", {"name": " "})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_project_rejects_invalid_json():
    response = client().post("/projects", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_list_projects_returns_creation_order():
    test_client = client()
    post_json(test_client, "/projects", {"name": "A"})
    post_json(test_client, "/projects", {"name": "B"})
    assert [project["name"] for project in test_client.get("/projects").get_json()] == ["A", "B"]


def test_create_task_under_project_returns_201():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    response = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Ship"})
    assert response.status_code == 201
    assert response.get_json()["project_id"] == project["id"]


def test_create_task_defaults_status_todo():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    task = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Ship"}).get_json()
    assert task["status"] == "todo"


def test_create_task_accepts_valid_status():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    task = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Ship", "status": "done"}).get_json()
    assert task["status"] == "done"


def test_create_task_rejects_invalid_status():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    response = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Ship", "status": "blocked"})
    assert response.status_code == 400


def test_create_task_rejects_blank_title():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    response = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": " "})
    assert response.status_code == 400


def test_create_task_for_missing_project_returns_404():
    response = post_json(client(), "/projects/999/tasks", {"title": "Ship"})
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_list_tasks_for_project():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Ship"})
    response = test_client.get(f"/projects/{project['id']}/tasks")
    assert [task["title"] for task in response.get_json()] == ["Ship"]


def test_list_tasks_filters_by_status():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "One", "status": "todo"})
    post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Two", "status": "done"})
    response = test_client.get(f"/projects/{project['id']}/tasks?status=done")
    assert [task["title"] for task in response.get_json()] == ["Two"]


def test_invalid_status_filter_returns_400():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    response = test_client.get(f"/projects/{project['id']}/tasks?status=blocked")
    assert response.status_code == 400


def test_update_task_title():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    task = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Old"}).get_json()
    response = test_client.patch(f"/tasks/{task['id']}", json={"title": "New"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "New"


def test_update_task_status():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    task = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Old"}).get_json()
    assert test_client.patch(f"/tasks/{task['id']}", json={"status": "done"}).get_json()["status"] == "done"


def test_update_missing_task_returns_404():
    response = client().patch("/tasks/999", json={"title": "New"})
    assert response.status_code == 404


def test_update_unknown_field_returns_400():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    task = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Old"}).get_json()
    assert test_client.patch(f"/tasks/{task['id']}", json={"owner": "me"}).status_code == 400


def test_delete_task_returns_204():
    test_client = client()
    project = post_json(test_client, "/projects", {"name": "A"}).get_json()
    task = post_json(test_client, f"/projects/{project['id']}/tasks", {"title": "Old"}).get_json()
    assert test_client.delete(f"/tasks/{task['id']}").status_code == 204


def test_delete_missing_task_returns_404():
    assert client().delete("/tasks/999").status_code == 404


def test_store_can_be_injected():
    store = InMemoryTaskStore()
    app = create_app(task_store=store)
    assert app.test_client().get("/health").status_code == 200


def test_405_response_is_json():
    response = client().put("/projects", json={"name": "A"})
    assert response.status_code == 405
    assert "error" in response.get_json()
