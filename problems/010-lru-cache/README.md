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

get returns value or None. put inserts or updates and evicts least recently used keys.

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
