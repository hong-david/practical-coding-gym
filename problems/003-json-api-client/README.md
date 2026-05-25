# 003 JSON API Client with Pagination and Retries

## Goal

Build a small API client around a fake paginated JSON API. Tests use fake transports and no real network calls.

## Files to Implement

```txt
src/
    api_client.py
```

## API/functions/classes expected

```python
class APIClient:
    def __init__(self, transport, max_retries=3): ...
    def fetch_all_items(self, endpoint: str) -> list[dict]: ...
    def fetch_item(self, endpoint: str, item_id: str) -> dict: ...
```

## Input/output shape

Transport `.get(endpoint)` returns `{ "items": [...], "next_page": "/api/items?page=2" }`.

## Level 1 MVP

Fetch all pages until next_page is None and preserve order.

## Level 2 Edge Cases

Retry transient errors and 429s, do not retry permanent 4xx errors, validate response shape, handle empty pages, duplicate IDs, bad responses, and missing items.

## Level 3 Senior Follow-Ups

Add backoff hooks, headers, idempotency, typed models, timeouts, cancellation, and logging.

## Provided test command

```bash
./scripts/test-problem.sh 003-json-api-client provided
```

## Custom test command

```bash
./scripts/test-problem.sh 003-json-api-client custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, edge cases, validation, error handling, source organization, mutation safety, test quality, usability, and simplicity.
