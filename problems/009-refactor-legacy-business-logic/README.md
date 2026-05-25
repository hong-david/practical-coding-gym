# 009 Refactor Legacy Business Logic

## Goal

Work with ugly but mostly working legacy pricing logic. Add tests, refactor safely, and add one new feature.

## Files to Implement

```txt
src/
    pricing_engine.py
```

## API/functions/classes expected

```python
calculate_price(plan, users, coupon=None, renewing=False) -> float
```

## Input/output shape

Plans are free, starter, pro, and enterprise. Coupons and renewal rules adjust final price.

## Level 1 MVP

Lock down existing behavior before refactoring.

## Level 2 Edge Cases

Preserve coupon ordering, renewal behavior, rounding, invalid plans, and add user-count validation.

## Level 3 Senior Follow-Ups

TODO: add ANNUAL20 coupon, then refactor duplicated branching into clearer tables/functions.

## Provided test command

```bash
./scripts/test-problem.sh 009-refactor-legacy-business-logic provided
```

## Custom test command

```bash
./scripts/test-problem.sh 009-refactor-legacy-business-logic custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
