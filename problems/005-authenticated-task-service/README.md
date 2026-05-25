# 005 Authenticated Task Service

## Goal

Practice users, login, token auth, ownership checks, and permission boundaries separately from the unauthenticated task service.

## Files to Implement

```txt
src/
    auth_task_service.py
```

## API/functions/classes expected

```python
class AuthTaskService with register_user, login, authenticated CRUD methods.
```

## Input/output shape

Users returned from `register_user(...)` are dictionaries with these minimum fields and no plaintext passwords:

```python
{
    "id": 1,
    "email": "user@example.com",
}
```

`login(email, password)` returns an opaque token string:

```python
"token-value"
```

Task IDs are global across all users. Task dictionaries include these minimum fields:

```python
{
    "id": 1,
    "owner_id": 1,
    "title": "Buy milk",
    "description": "",
}
```

`create_task(...)`, `get_task(...)`, and `update_task(...)` return one task dictionary. `list_tasks(token)` returns only the authenticated user's task dictionaries. `delete_task(...)` returns `True` when an owned task is deleted.

Expected errors:

- duplicate normalized emails raise `ValueError`
- blank email or password raises `ValueError`
- invalid login credentials raise `PermissionError`
- invalid tokens raise `PermissionError`
- cross-user read/update/delete attempts raise `PermissionError`
- blank task titles raise `ValueError`

Returned user/task dictionaries must not expose mutable internal state.

Example expected behavior:

```python
service = AuthTaskService()

alice = service.register_user("Alice@Example.com", "secret")
token = service.login("alice@example.com", "secret")

task = service.create_task(token, "Ship feature")
task["owner_id"] == alice["id"]

service.list_tasks(token)[0]["id"] == task["id"]

bob = service.register_user("bob@example.com", "secret")
bob_token = service.login("bob@example.com", "secret")
service.get_task(bob_token, task["id"])  # raises PermissionError
```

## Level 1 MVP

Register, login, create/list/get/update/delete owned tasks.

## Level 2 Edge Cases

Reject duplicate users, blank passwords, invalid tokens, cross-user access, invalid task input, and mutation leaks.

## Level 3 Senior Follow-Ups

Hash passwords, expire tokens, add roles, audit logs, refresh tokens, and API adapters.

## Provided test command

```bash
./scripts/test-problem.sh 005-authenticated-task-service provided
```

## Custom test command

```bash
./scripts/test-problem.sh 005-authenticated-task-service custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
