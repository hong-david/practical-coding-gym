# 013 Background Job Queue

## Goal

Build an in-memory FIFO job queue with retries and dead-letter behavior.

## Files to Implement

```txt
src/
    job_queue.py
```

## API/functions/classes expected

```python
class JobQueue with enqueue, reserve_next, complete, fail, dead_letters.
```

## Input/output shape

Jobs are dictionaries:

```python
{
    "id": 1,
    "job_type": "email",
    "payload": {"to": "a@example.com"},
    "status": "queued",  # queued, running, completed, retry_scheduled, dead_lettered
    "attempts": 0,
    "last_error": None,
}
```

`enqueue(job_type, payload)` returns the queued job dictionary.

`reserve_next()` returns the next queued job in FIFO order, marks it `running`, increments `attempts`, and returns `None` when no queued jobs are available.

`complete(job_id)` returns `None` and marks a running job completed.

`fail(job_id, reason)` returns `None`. Failed jobs are requeued until `max_attempts` is reached; after that they move to the dead-letter list.

`dead_letters()` returns a copy of dead-lettered job dictionaries.

Expected errors:

- non-positive `max_attempts` raises `ValueError`
- blank job type raises `ValueError`
- non-dictionary payload raises `TypeError`
- completing/failing unknown jobs raises `KeyError`
- completing the same job twice raises `ValueError`
- blank failure reasons raise `ValueError`

Payloads and returned job dictionaries should be copies where mutation would otherwise leak into internal state.

Example expected behavior:

```python
queue = JobQueue(max_attempts=2)

job = queue.enqueue("email", {"to": "a@example.com"})
job["status"] == "queued"

reserved = queue.reserve_next()
reserved["id"] == job["id"]
reserved["status"] == "running"
reserved["attempts"] == 1

queue.fail(job["id"], "temporary outage")
queue.reserve_next()["id"] == job["id"]

queue.complete(job["id"]) is None
queue.reserve_next() is None
```

## Level 1 MVP

Enqueue, reserve FIFO, complete, and retry failures.

## Level 2 Edge Cases

Validate input, unknown jobs, double completion, retry limits, payload preservation, and dead-letter copies.

## Level 3 Senior Follow-Ups

Add visibility timeouts, delayed jobs, workers, persistence, metrics, idempotency, and thread safety.

## Provided test command

```bash
./scripts/test-problem.sh 013-background-job-queue provided
```

## Custom test command

```bash
./scripts/test-problem.sh 013-background-job-queue custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
