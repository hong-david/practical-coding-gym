# 004 REST API Tasks Service

## Goal

Build a framework-free in-memory task service with CRUD-style behavior.

## Files to Implement

```txt
src/
    task_service.py
```

## API/functions/classes expected

```python
class TaskService with create_task, get_task, list_tasks, update_task, delete_task.
```

## Input/output shape

Tasks are dictionaries:

```python
{
    "id": 1,
    "title": "Buy milk",
    "description": "",
    "status": "todo",
    "created_at": "2026-05-01T10:00:00Z",
    "updated_at": "2026-05-01T10:00:00Z",
}
```

`create_task(...)`, `get_task(...)`, and `update_task(...)` return one task dictionary.

`list_tasks(status=None)` returns a list of task dictionaries in creation order:

```python
[
    {"id": 1, "title": "A", ...},
    {"id": 2, "title": "B", ...},
]
```

`delete_task(task_id)` returns `True` when an existing task is deleted and `False` when the task does not exist.

Returned task dictionaries must be copies. Mutating a returned dictionary must not mutate internal service state.

Expected errors:

- blank titles raise `ValueError`
- invalid status values raise `ValueError`
- unknown fields in `update_task(...)` raise `ValueError`
- missing tasks for `get_task(...)` or `update_task(...)` raise `KeyError`

Example expected behavior:

```python
service = TaskService()

created = service.create_task("Buy milk")
created["id"] == 1
created["status"] == "todo"

service.update_task(1, status="done")["status"] == "done"
service.list_tasks(status="done") == [service.get_task(1)]
service.delete_task(1) is True
service.delete_task(1) is False
```

## Level 1 MVP

Create, retrieve, list, update, and delete tasks in memory.

## Level 2 Edge Cases

Validate title, status, filtering, unknown fields, deletion, timestamps, and mutation safety.

## Level 3 Senior Follow-Ups

Add persistence, deterministic clocks, API routes, sorting, search, and optimistic concurrency.

## Provided test command

```bash
./scripts/test-problem.sh 004-rest-api-tasks provided
```

## Custom test command

```bash
./scripts/test-problem.sh 004-rest-api-tasks custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
