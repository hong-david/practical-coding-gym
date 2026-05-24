# 001 Log Analyzer

## Goal

Build a command-line log analyzer that reads server log data and returns request statistics.

This problem focuses on:

- file reading
- text parsing
- malformed input handling
- aggregation
- custom tests
- CLI behavior
- separating core logic from I/O

---

## Files to Implement

Suggested source layout:

```txt
src/
    log_analyzer.py
    main.py
```

Expected functions:

```python
analyze_log_text(text: str) -> dict
analyze_log_file(filepath: str) -> dict
```

`log_analyzer.py` should contain parsing and aggregation logic.

`main.py` should contain CLI behavior.

Avoid putting all logic directly in `main.py`.

---

## Log Format

Each valid log line has exactly 7 fields:

```txt
timestamp level ip method path status duration_ms
```

Example:

```txt
2026-05-24T10:15:30Z INFO 192.168.1.10 GET /api/users 200 34ms
```

| Field | Example | Rule |
|---|---|---|
| timestamp | `2026-05-24T10:15:30Z` | non-empty string |
| level | `INFO` | non-empty string |
| ip | `192.168.1.10` | non-empty string |
| method | `GET` | allowed HTTP method |
| path | `/api/users` | must start with `/` |
| status | `200` | integer from 100 to 599 |
| duration_ms | `34ms` | digits followed by `ms` |

Allowed HTTP methods:

```txt
GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD
```

---

## Counting Rules

Blank lines are ignored completely.

Blank lines should not count as:

- total lines
- valid lines
- malformed lines

`total_lines` means total non-blank lines processed.

Malformed lines should not crash the program.

Malformed lines should increase `malformed_lines`, but should not contribute to:

- `status_codes`
- `methods`
- `paths`

---

## Level 1: MVP

Implement:

```python
analyze_log_text(text: str) -> dict
```

Return this shape:

```python
{
    "total_lines": 5,
    "valid_lines": 5,
    "malformed_lines": 0,
    "status_codes": {
        200: 2,
        302: 1,
        404: 1,
        500: 1,
    },
    "methods": {
        "GET": 4,
        "POST": 1,
    },
    "paths": {
        "/api/users": 2,
        "/login": 1,
        "/missing": 1,
        "/api/orders": 1,
    },
}
```

Requirements:

- parse valid log lines
- count total non-blank lines
- count valid lines
- count malformed lines
- count status codes
- count HTTP methods
- count paths
- ignore blank lines
- do not crash on malformed lines

---

## Level 2: Edge Cases

Handle:

- extra whitespace between fields
- empty files
- missing fields
- too many fields
- invalid status codes
- status codes outside `100-599`
- durations that do not end in `ms`
- durations with non-numeric values
- unknown HTTP methods
- paths that do not start with `/`
- mixed valid and invalid lines

---

## Level 3: Senior Follow-Ups

Add:

```python
analyze_log_file(filepath: str) -> dict
```

Requirements:

- read logs from a file
- raise a clear `FileNotFoundError` for missing files
- keep file I/O separate from text parsing

Add a CLI:

```bash
python problems/001-log-analyzer/src/main.py problems/001-log-analyzer/fixtures/simple.log
```

CLI requirements:

- accept a filepath argument
- print the summary
- return a nonzero exit code on bad usage or missing file
- avoid dumping an ugly traceback for expected user errors

Optional follow-ups:

- `--status 500`
- `--method GET`
- `--top-paths 3`
- `--json`
- stream large files line by line

---

## Provided Tests

Provided tests live in:

```txt
tests/provided/
```

Run provided tests from the repo root:

```bash
./scripts/test-problem.sh 001-log-analyzer provided
```

Direct command:

```bash
python -m pytest problems/001-log-analyzer/tests/provided
```

Provided tests are the baseline contract.

---

## Custom Tests

Add custom tests in:

```txt
tests/custom/
```

Example:

```txt
tests/custom/test_my_cases.py
```

Run custom tests:

```bash
./scripts/test-problem.sh 001-log-analyzer custom
```

Run all tests for this problem:

```bash
./scripts/test-problem.sh 001-log-analyzer
```

Good custom test ideas:

- one valid line
- one malformed line
- empty input
- repeated status codes
- repeated paths
- unknown HTTP method
- invalid duration
- invalid path
- missing file
- CLI with no arguments
- CLI with a missing file
- CLI with a valid fixture

---

## Manual Runs

Run the CLI manually:

```bash
python problems/001-log-analyzer/src/main.py problems/001-log-analyzer/fixtures/simple.log
```

Other useful checks:

```bash
python problems/001-log-analyzer/src/main.py problems/001-log-analyzer/fixtures/mixed.log
python problems/001-log-analyzer/src/main.py problems/001-log-analyzer/fixtures/empty.log
python problems/001-log-analyzer/src/main.py problems/001-log-analyzer/fixtures/does_not_exist.log
```

---

## Suggested Approach

One reasonable implementation path:

1. Create an empty summary dictionary.
2. Split input text into lines.
3. Ignore blank lines.
4. Parse each non-blank line.
5. Validate field count.
6. Validate method, path, status, and duration.
7. Count valid lines.
8. Count malformed lines.
9. Aggregate status codes, methods, and paths.
10. Add file reading.
11. Add CLI behavior.
12. Add custom tests.

Possible helper functions:

```python
parse_log_line(line: str)
is_valid_method(method: str) -> bool
is_valid_status(status: str) -> bool
is_valid_duration(duration: str) -> bool
empty_summary() -> dict
```

Keep the implementation simple.

---

## Git Workflow

Recommended branch:

```bash
git checkout main
git pull
git checkout -b solve-001-log-analyzer
```

Useful commands:

```bash
git status
git diff
git add problems/001-log-analyzer
git diff --staged
git commit -m "Implement log analyzer MVP"
```

Push when ready:

```bash
git push -u origin solve-001-log-analyzer
```

Open a PR and send the PR URL for review.

---

## PR Review Checklist

Review should check:

- correctness against this README
- missing requirements
- malformed input handling
- edge cases
- error handling
- separation of parsing from file I/O
- separation of CLI code from business logic
- readability
- function boundaries
- test quality
- usefulness of custom tests
- command-line usability
- simplicity vs overengineering
- senior-level judgment

---

## Definition of Done

This problem is complete when:

- provided tests pass
- custom tests pass
- CLI works manually
- malformed input does not crash the analyzer
- missing files produce a clear error
- code is organized into reasonable functions
- PR has been reviewed and revised
