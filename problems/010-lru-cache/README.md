# 010 LRU Cache

## Goal

Implement an in-memory LRU cache.

## Files to Implement

```txt
src/
    lru_cache.py
```

## API/functions/classes expected

```python
class LRUCache with __init__, get, and put.
```

## Input/output shape

`LRUCache(capacity)` creates an empty cache with a positive maximum size.

```python
cache = LRUCache(2)
```

`put(key, value)` inserts or updates a key and returns `None`:

```python
cache.put("a", 1) is None
```

`get(key)` returns the stored value or `None` when the key is missing:

```python
cache.get("a") == 1
cache.get("missing") is None
```

Recency rules:

- `get(existing_key)` makes that key most recently used
- `put(existing_key, value)` updates the value and makes that key most recently used
- inserting beyond capacity evicts the least recently used key

Falsey values such as `None`, `False`, and `0` can be stored. In this lab, `None` is also the missing-key sentinel, so callers cannot distinguish stored `None` from missing by return value alone.

Expected errors:

- zero or negative capacity raises `ValueError`

## Level 1 MVP

Support basic get/put and eviction.

## Level 2 Edge Cases

Validate capacity, refresh recency on get/update, handle falsey values and hashable keys.

## Level 3 Senior Follow-Ups

Use an O(1) conceptual design, usually dictionary plus linked order or OrderedDict.

## Provided test command

```bash
./scripts/test-problem.sh 010-lru-cache provided
```

## Custom test command

```bash
./scripts/test-problem.sh 010-lru-cache custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
