# 015 Code Review Lab

## Goal

Practice reviewing a flawed PR. The goal is to write `review.md`, not just to make tests pass.

## Files to Implement

```txt
src/
    submitted_solution.py
review_materials/
    fake_pr_description.md
    expected_review_points.md
```

## API/functions/classes expected

```python
summarize_orders(orders: list[dict]) -> dict
```

## Input/output shape

Orders contain customer, quantity, price, and status. The submitted solution returns totals by customer but has realistic flaws.

## Level 1 MVP

Read the fake PR, inspect the code, run tests, and write review.md with findings.

## Level 2 Edge Cases

Look for missing edge cases, unclear names, duplicated logic, bad error handling, weak tests, mutation bugs, and performance concerns.

## Level 3 Senior Follow-Ups

Compare your review to expected_review_points.md, then optionally revise the submitted solution after the review.

## Provided test command

```bash
./scripts/test-problem.sh 015-code-review-lab provided
```

## Custom test command

```bash
./scripts/test-problem.sh 015-code-review-lab custom
```

## Manual run command

```bash
python -m pytest problems/015-code-review-lab/tests/provided
```

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
