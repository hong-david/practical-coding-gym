# 007 Fullstack Message Board

## Goal

Scaffold a fullstack-style lab, but keep it runnable without external databases.

## Files to Implement

```txt
src/
    message_board.py
```

## API/functions/classes expected

```python
class MessageBoard with create_user, create_post, list_posts, add_comment, delete_post, delete_comment.
```

## Input/output shape

Users are dictionaries:

```python
{
    "id": 1,
    "username": "alice",
}
```

Posts are dictionaries:

```python
{
    "id": 1,
    "user_id": 1,
    "title": "Hello",
    "body": "Post body",
    "comments": [],
    "created_at": "...",
}
```

Comments are dictionaries:

```python
{
    "id": 1,
    "post_id": 1,
    "user_id": 1,
    "body": "Nice post",
    "created_at": "...",
}
```

`create_user(...)`, `create_post(...)`, and `add_comment(...)` return the created dictionary. `list_posts(limit=20, offset=0)` returns post dictionaries newest-first. `delete_post(...)` and `delete_comment(...)` return `True` when deletion succeeds.

Expected errors:

- blank usernames, titles, bodies, or comments raise `ValueError`
- duplicate usernames raise `ValueError`
- missing users/posts/comments raise `KeyError`
- deleting another user's post/comment raises `PermissionError`
- invalid pagination values raise `ValueError`

Returned dictionaries/lists must be copies, not references to internal state.

Example expected behavior:

```python
board = MessageBoard()

alice = board.create_user("alice")
post = board.create_post(alice["id"], "Hello", "First post")
comment = board.add_comment(alice["id"], post["id"], "Nice")

board.list_posts(limit=10, offset=0)[0]["id"] == post["id"]
board.delete_comment(alice["id"], comment["id"]) is True
board.delete_post(alice["id"], post["id"]) is True
```

## Level 1 MVP

Create users/posts/comments and list posts with pagination.

## Level 2 Edge Cases

Validate blank input, missing records, ownership, pagination bounds, deletion, and mutation safety.

## Level 3 Senior Follow-Ups

Add persistence, API routes, auth, moderation, search, edit history, and rate limits.

## Provided test command

```bash
./scripts/test-problem.sh 007-fullstack-message-board provided
```

## Custom test command

```bash
./scripts/test-problem.sh 007-fullstack-message-board custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
