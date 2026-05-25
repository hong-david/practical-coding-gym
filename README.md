# Practical Coding Gym

Using this repo as my personal practice environment for building things 0->1 manually, boutique hand-coding if you will.
The goal is not just to solve isolated algorithm problems. I'm setting this up as:

- reading requirements
- building applications from scratch
- command line / Git practice
- writing and running tests
- debugging failures, handling edge cases
- PR review with ChatGPT

Each problem is designed to start with a simple MVP, then expand into realistic edge cases and senior-level follow-ups.

---

## Repo Structure

```txt
practical-coding-gym/
    README.md
    requirements.txt
    scripts/
        test-problem.sh
    problems/
        001-log-analyzer/
        002-csv-transaction-reconciler/
        ...
        015-code-review-lab/
```

Each problem generally follows:

```txt
problems/<number>-<slug>/
    README.md
    fixtures/
    src/
        <main_module>.py
        main.py              # only when CLI makes sense
    tests/
        provided/
            test_<main_module>.py
        custom/
            README.md
```

## Problems

- 001 Log Analyzer
- 002 CSV Transaction Reconciler
- 003 JSON API Client with Pagination and Retries
- 004 REST API Tasks Service
- 005 Authenticated Task Service
- 006 Frontend Developer Portal
- 007 Fullstack Message Board
- 008 Debugging Existing Codebase
- 009 Refactor Legacy Business Logic
- 010 LRU Cache
- 011 Rate Limiter
- 012 Async Task Runner
- 013 Background Job Queue
- 014 Search and Ranking Service
- 015 Code Review Lab

## Running Tests

Use the generic test script (tests all) or add provided/custom flag:

```bash
./scripts/test-problem.sh <problem-folder>
./scripts/test-problem.sh <problem-folder> provided
./scripts/test-problem.sh <problem-folder> custom
```
