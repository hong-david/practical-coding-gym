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

Jobs have IDs, statuses, attempt counts, payloads, and failure reasons. Failed jobs retry up to max_attempts then move to dead letters.

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
