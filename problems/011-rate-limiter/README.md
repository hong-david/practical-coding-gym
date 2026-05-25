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

The fake clock must expose:

```python
clock.now() -> number
```

`FixedWindowRateLimiter(limit, window_seconds, clock)` tracks accepted requests per user in fixed epoch-aligned windows.

`allow(user_id)` returns a boolean:

```python
True   # request accepted
False  # user exceeded the limit in the current window
```

Behavior:

- each user has an independent counter
- exactly `limit` requests are allowed per window
- the next request in the same window returns `False`
- counters reset when `clock.now()` moves into a new window
- blocked requests do not block other users

Expected errors:

- non-positive `limit` raises `ValueError`
- non-positive `window_seconds` raises `ValueError`
- missing `clock.now` raises `TypeError`
- blank user IDs raise `ValueError`

Example expected behavior:

```python
clock = FakeClock(now=0)
limiter = FixedWindowRateLimiter(limit=2, window_seconds=60, clock=clock)

limiter.allow("alice") is True
limiter.allow("alice") is True
limiter.allow("alice") is False

limiter.allow("bob") is True

clock.advance(60)
limiter.allow("alice") is True
```

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
