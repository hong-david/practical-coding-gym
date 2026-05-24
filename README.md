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
            README.md
            fixtures/
            src/
            tests/
                provided/
                custom/
```
## Running Tests

Use the generic test script (tests all) or add provided/custom flag:

```bash
./scripts/test-problem.sh <problem-folder>
./scripts/test-problem.sh <problem-folder> provided
./scripts/test-problem.sh <problem-folder> custom
```