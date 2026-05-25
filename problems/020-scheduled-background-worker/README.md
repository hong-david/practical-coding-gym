# 020 Scheduled Background Worker

## Goal

Build an in-memory background worker that supports scheduling jobs for the future, delays, timeouts, retries, and deterministic fake-clock tests. This is about worker orchestration, not async syntax.

## Files to Implement

```txt
src/
    scheduled_worker.py
fixtures/
```

## API/functions/classes expected

```python
class ScheduledWorker:
    def __init__(self, clock, max_attempts: int = 3, default_timeout_seconds: int = 30): ...
    def enqueue_at(self, job_type: str, payload: dict, run_at: float, timeout_seconds: int | None = None) -> dict: ...
    def enqueue_in(self, job_type: str, payload: dict, delay_seconds: float, timeout_seconds: int | None = None) -> dict: ...
    def cancel(self, job_id: int) -> bool: ...
    def run_due(self, handlers: dict[str, callable]) -> list[dict]: ...
    def get_job(self, job_id: int) -> dict: ...
    def dead_letters(self) -> list[dict]: ...
```

## Input/output shape

The fake clock must expose:

```python
clock.now() -> number
```

Jobs are dictionaries:

```python
{
    "id": 1,
    "job_type": "email",
    "payload": {"to": "a@example.com"},
    "run_at": 100.0,
    "timeout_seconds": 30,
    "attempts": 0,
    "status": "queued",  # queued, running, completed, retry_scheduled, cancelled, dead_lettered
    "last_error": None,
    "created_at": 0.0,
    "updated_at": 0.0,
}
```

`enqueue_at(...)` and `enqueue_in(...)` return queued job dictionaries.

`run_due(handlers)` runs due, non-cancelled jobs in scheduled order. Jobs with the same `run_at` run FIFO. `handlers` maps job type strings to callables:

```python
{"email": lambda payload: "sent"}
```

`run_due(...)` returns job records for jobs it processed. Successful jobs are marked `completed`. Failed jobs are marked `retry_scheduled` until `max_attempts` is reached, then moved to dead letters.

`cancel(job_id)` returns `True` when a queued job is cancelled and `False` for unknown jobs.

`get_job(job_id)` returns one job dictionary. `dead_letters()` returns a copy of dead-lettered job dictionaries.

Expected errors:

- non-positive `max_attempts` raises `ValueError`
- clock without `now()` raises `TypeError`
- blank job types raise `ValueError`
- non-dictionary payloads raise `TypeError`
- negative delays raise `ValueError`
- non-positive timeouts raise `ValueError`
- unknown job IDs in `get_job(...)` raise `KeyError`

Timeout failures are represented with `JobTimeoutError`.

## Level 1 MVP

Enqueue delayed jobs, run only due jobs, execute handlers, complete successful jobs, and expose job status.

## Level 2 Edge Cases

Handle FIFO order for same scheduled time, cancellation, missing handlers, retries after failure, max-attempt dead letters, per-job timeouts, invalid delays/timeouts, payload copy safety, and fake-clock determinism.

## Level 3 Senior Follow-Ups

Add persistent storage, worker heartbeats, visibility timeouts, exponential backoff, recurring jobs, metrics, poison-job alerts, and graceful shutdown semantics.

## Provided test command

```bash
./scripts/test-problem.sh 020-scheduled-background-worker provided
```

## Custom test command

```bash
./scripts/test-problem.sh 020-scheduled-background-worker custom
```

## Manual run command

```bash
python -m pytest problems/020-scheduled-background-worker/tests/provided
```

## Definition of Done

Provided tests pass, custom tests cover at least one retry or timeout scenario, and the worker is deterministic under fake clocks.

## PR Review Checklist

Check scheduling semantics, retry/dead-letter behavior, timeout handling, fake-clock usage, payload copying, handler isolation, state transitions, and whether worker code is testable without sleeping.
