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

Documents are added with:

```python
add_document(doc_id="1", title="Python Guide", body="Learn testing", tags=["python"])
```

Stored document shape:

```python
{
    "doc_id": "1",
    "title": "Python Guide",
    "body": "Learn testing",
    "tags": ["python"],
}
```

`search(query, tags=None, limit=10, offset=0)` returns ranked result dictionaries:

```python
[
    {
        "doc_id": "1",
        "title": "Python Guide",
        "score": 3,
    },
]
```

Ranking rules:

- token matching is case-insensitive
- title matches score higher than body matches
- documents matching more query terms rank higher
- ties are resolved by insertion order
- tag filters require all requested tags

Behavior:

- empty or blank queries return `[]`
- duplicate `doc_id` updates the existing document
- returned result dictionaries must not expose mutable internal state

Expected errors:

- blank document IDs raise `ValueError`
- documents with both blank title and blank body raise `ValueError`
- non-positive `limit` raises `ValueError`
- negative `offset` raises `ValueError`

Example expected behavior:

```python
search = SearchService()
search.add_document("1", "Python Guide", "Learn testing", tags=["python"])
search.add_document("2", "Testing", "Python pytest tips", tags=["python", "testing"])

results = search.search("python", tags=["testing"])

results == [
    {
        "doc_id": "2",
        "title": "Testing",
        "score": 2,
    },
]
```

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
