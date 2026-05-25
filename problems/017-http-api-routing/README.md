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

The app should expose JSON routes for `/health`, `/projects`, `/projects/<id>/tasks`, and `/tasks/<id>`. Successful responses are JSON objects or arrays. Error responses should be JSON with an `error` key and appropriate HTTP status codes.

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
