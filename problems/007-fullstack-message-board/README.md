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

Users, posts, and comments are dictionaries with generated IDs. Owners can delete their own posts/comments.

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
