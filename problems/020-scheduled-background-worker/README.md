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

Jobs include `id`, `job_type`, `payload`, `run_at`, `timeout_seconds`, `attempts`, `status`, `last_error`, and timestamps. `run_due` returns completed, retried, timed-out, or dead-lettered job records.

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
