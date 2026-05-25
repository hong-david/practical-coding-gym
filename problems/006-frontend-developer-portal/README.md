# 006 Frontend Developer Portal

## Goal

Scaffold a frontend/API-integration lab using pure state and API-adapter functions testable with pytest. A minimal JS placeholder is included because the lab is frontend-framed.

## Files to Implement

```txt
src/
    developer_portal.py
```

## API/functions/classes expected

```python
login, auth_headers, create_initial_state, reducer, fetch_all_pages, update_resource.
```

## Input/output shape

State tracks token, loading, error, apps, resources, and users. Fake API objects expose get/post/patch.

## Level 1 MVP

Implement login, token use, state reducer, pagination, and resource updates.

## Level 2 Edge Cases

Handle blank inputs, loading/error states, unknown actions, immutable reducer behavior, and malformed API responses.

## Level 3 Senior Follow-Ups

Port the pure logic to JavaScript, wire it to DOM/React, add optimistic updates, cancellation, and accessibility checks.

## Provided test command

```bash
./scripts/test-problem.sh 006-frontend-developer-portal provided
```

## Custom test command

```bash
./scripts/test-problem.sh 006-frontend-developer-portal custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
