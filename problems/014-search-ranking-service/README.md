# 014 Search and Ranking Service

## Goal

Build a small in-memory search service over documents.

## Files to Implement

```txt
src/
    search_service.py
```

## API/functions/classes expected

```python
class SearchService with add_document and search.
```

## Input/output shape

Documents have IDs, title, body, and tags. Search returns ranked dictionaries including doc_id, title, and score. Duplicate IDs update existing docs.

## Level 1 MVP

Index documents and search title/body tokens case-insensitively.

## Level 2 Edge Cases

Handle ranking, tie-breaking, tags, pagination, empty queries, duplicate IDs, validation, and mutation safety.

## Level 3 Senior Follow-Ups

Add stemming, phrase search, highlighting, field boosts, deletion, incremental indexes, and profiling.

## Provided test command

```bash
./scripts/test-problem.sh 014-search-ranking-service provided
```

## Custom test command

```bash
./scripts/test-problem.sh 014-search-ranking-service custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
