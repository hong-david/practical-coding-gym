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

Emails are normalized. Login returns tokens. Task IDs are global and tasks include owner_id. Users can only access their own tasks.

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
