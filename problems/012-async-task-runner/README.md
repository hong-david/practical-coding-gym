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

`tasks` is an iterable of callables. Each callable must return an awaitable:

```python
async def work():
    return "done"

tasks = [lambda: work()]
```

`run_tasks(tasks, concurrency_limit)` returns a list with one result slot per input task, preserving input order:

```python
["first-result", "second-result"]
```

Concurrency behavior:

- at most `concurrency_limit` tasks may be running at once
- a larger limit than the number of tasks is allowed
- the input task collection must not be mutated

Failure behavior:

- coroutine exceptions are captured clearly in the corresponding result slot
- synchronous exceptions raised while creating a coroutine are captured clearly
- cancellation should be represented clearly in the corresponding result slot

Expected errors:

- non-positive concurrency limits raise `ValueError`
- `tasks=None` raises `TypeError`
- non-callable tasks raise `TypeError`
- callables that do not return awaitables raise `TypeError`

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
