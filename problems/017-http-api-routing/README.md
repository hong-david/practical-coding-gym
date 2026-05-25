# 017 HTTP API Routing

## Goal

Build a small HTTP JSON API for projects and tasks using Flask, FastAPI, or a similar lightweight framework. This is an API-routing lab, not a database lab; persistence can be an injected in-memory store.

## Files to Implement

```txt
src/
    task_api.py
fixtures/
```

## API/functions/classes expected

```python
def create_app(task_store=None):
    ...

class InMemoryTaskStore:
    def create_project(self, name: str) -> dict: ...
    def list_projects(self) -> list[dict]: ...
    def create_task(self, project_id: int, title: str, status: str = "todo") -> dict: ...
    def list_tasks(self, project_id: int | None = None, status: str | None = None) -> list[dict]: ...
    def update_task(self, task_id: int, **updates) -> dict: ...
    def delete_task(self, task_id: int) -> bool: ...
```

## Input/output shape

The app exposes JSON routes:

```txt
GET    /health
GET    /projects
POST   /projects
GET    /projects/<project_id>/tasks
POST   /projects/<project_id>/tasks
PATCH  /tasks/<task_id>
DELETE /tasks/<task_id>
```

Project shape:

```python
{
    "id": 1,
    "name": "Platform",
}
```

Task shape:

```python
{
    "id": 1,
    "project_id": 1,
    "title": "Ship feature",
    "status": "todo",  # todo, in_progress, done
}
```

Response expectations:

- `GET /health` returns `200` and `{"status": "ok"}`
- `POST /projects` returns `201` and one project
- `GET /projects` returns project dictionaries in creation order
- `POST /projects/<id>/tasks` returns `201` and one task
- `GET /projects/<id>/tasks` returns task dictionaries, optionally filtered by `?status=done`
- `PATCH /tasks/<id>` returns `200` and the updated task
- `DELETE /tasks/<id>` returns `204` with no body

Error responses must be JSON dictionaries with an `error` key:

```python
{"error": "message"}
```

Expected status codes:

- invalid JSON or validation errors return `400`
- missing projects/tasks return `404`
- unsupported methods return `405` with JSON error shape

Example expected behavior:

```python
app = create_app()
client = app.test_client()

client.get("/health").get_json() == {"status": "ok"}

project_response = client.post("/projects", json={"name": "Platform"})
project_response.status_code == 201
project = project_response.get_json()

task_response = client.post(
    f"/projects/{project['id']}/tasks",
    json={"title": "Ship API", "status": "todo"},
)
task_response.status_code == 201

client.get(f"/projects/{project['id']}/tasks?status=todo").get_json() == [
    task_response.get_json()
]
```

## Level 1 MVP

Implement an app factory, health route, project creation/listing, task creation/listing, task update, and task deletion.

## Level 2 Edge Cases

Handle invalid JSON, blank names/titles, invalid statuses, missing projects/tasks, status filtering, wrong content types, method-not-allowed behavior, consistent error shape, no traceback leakage, and stable response codes.

## Level 3 Senior Follow-Ups

Add request IDs, structured logging, pagination, OpenAPI docs, dependency injection for stores, auth middleware, integration tests, and production configuration separation.

## Provided test command

```bash
./scripts/test-problem.sh 017-http-api-routing provided
```

## Custom test command

```bash
./scripts/test-problem.sh 017-http-api-routing custom
```

## Manual run command

```bash
python -m pytest problems/017-http-api-routing/tests/provided
```

## Definition of Done

Provided tests pass, custom tests cover at least one new route/error case, and manual route checks return JSON with correct status codes.

## PR Review Checklist

Check route semantics, HTTP status codes, JSON error consistency, validation, dependency injection, store isolation between tests, framework-specific best practices, and whether transport code is separated from business logic.
