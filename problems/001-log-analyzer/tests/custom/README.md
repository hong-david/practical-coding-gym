# Custom Tests

Add your own tests in this folder.

Example filename:

```txt
test_my_log_analyzer_cases.py
```

Run custom tests from the repo root:

```bash
make test-001-custom
```

Run all tests for this problem:

```bash
make test-001
```

Suggested custom test ideas:

- one valid line
- one malformed line
- empty input
- repeated paths
- repeated status codes
- invalid method
- invalid status
- invalid duration
- file not found
- CLI argument behavior
