# 012 Async Task Runner

## Goal

Implement async task execution with a concurrency limit.

## Files to Implement

```txt
src/
    async_task_runner.py
```

## API/functions/classes expected

```python
async def run_tasks(tasks, concurrency_limit: int) -> list
```

## Input/output shape

Tasks is an iterable of callables returning awaitables. Results preserve input order and failures are captured clearly.

## Level 1 MVP

Run tasks with at most N active tasks.

## Level 2 Edge Cases

Validate limits and task shapes, handle factory/coroutine exceptions, cancellation, many tasks, and input immutability.

## Level 3 Senior Follow-Ups

Add fatal cancellation modes, timeouts, progress callbacks, structured results, and graceful shutdown.

## Provided test command

```bash
./scripts/test-problem.sh 012-async-task-runner provided
```

## Custom test command

```bash
./scripts/test-problem.sh 012-async-task-runner custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
