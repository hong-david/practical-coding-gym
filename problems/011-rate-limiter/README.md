# 011 Rate Limiter

## Goal

Implement rate limiting with fake clocks, not real sleep.

## Files to Implement

```txt
src/
    rate_limiter.py
```

## API/functions/classes expected

```python
class FixedWindowRateLimiter with __init__ and allow. Optional TokenBucketRateLimiter follow-up.
```

## Input/output shape

allow returns True for accepted requests and False when a user exceeds the current fixed window.

## Level 1 MVP

Track request counts per user per window.

## Level 2 Edge Cases

Handle boundaries, multiple users, invalid config, blank users, reset behavior, and independence between users.

## Level 3 Senior Follow-Ups

Add token bucket behavior, retry-after metadata, cleanup, persistence, and thread safety.

## Provided test command

```bash
./scripts/test-problem.sh 011-rate-limiter provided
```

## Custom test command

```bash
./scripts/test-problem.sh 011-rate-limiter custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
