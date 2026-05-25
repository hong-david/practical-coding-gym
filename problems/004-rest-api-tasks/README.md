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

Tasks are dictionaries with id, title, description, status, created_at, and updated_at. Deleting nonexistent tasks returns False.

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
