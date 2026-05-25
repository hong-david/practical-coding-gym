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

State dictionaries have this shape:

```python
{
    "token": None,
    "loading": False,
    "error": None,
    "apps": [],
    "resources": [],
    "users": [],
}
```

Fake API objects expose:

```python
api.post(path: str, payload: dict, headers: dict | None = None) -> dict
api.get(path: str, headers: dict | None = None) -> dict
api.patch(path: str, payload: dict, headers: dict | None = None) -> dict
```

`login(api, email, password)` returns the API login response, expected to include a token:

```python
{"token": "token-value"}
```

`auth_headers(token)` returns:

```python
{"Authorization": "Bearer token-value"}
```

`fetch_all_pages(api, path)` expects paginated responses:

```python
{"items": [{...}], "next_page": "/next-page-or-null"}
```

and returns one flat list of item dictionaries.

`update_resource(api, token, resource_id, updates)` returns the API patch response dictionary.

`reducer(state, action)` returns a new state dictionary and must not mutate the input state. Unknown action types raise `ValueError`.

Example expected behavior:

```python
state = create_initial_state()
state["loading"] is False

loading_state = reducer(state, {"type": "login_started"})
loading_state["loading"] is True
state["loading"] is False  # original state was not mutated

auth_headers("abc") == {"Authorization": "Bearer abc"}

fetch_all_pages(api, "/apps") == [
    {"id": "app-1"},
    {"id": "app-2"},
]
```

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
