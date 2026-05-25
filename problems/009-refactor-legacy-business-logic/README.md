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

`calculate_price(plan, users, coupon=None, renewing=False)` returns the final price as a two-decimal numeric value:

```python
calculate_price("starter", 1) == 19
calculate_price("pro", 1, "SAVE10", True) == 41.9
```

Supported plans and base prices:

```python
{
    "free": 0,
    "starter": 19,
    "pro": 49,
    "enterprise": 199,
}
```

For paid plans, each additional user after the first adds `5`.

Supported coupons:

```python
{
    "SAVE10": "10 percent off",
    "HALF": "50 percent off",
    "ANNUAL20": "20 percent off new feature",
}
```

Unknown coupons are ignored for legacy compatibility. Renewal discounts apply only to `pro` and `enterprise` plans. Coupon discounts are applied before renewal discounts.

Expected errors:

- unknown plan names raise `ValueError`
- zero or negative users raise `ValueError`
- plan names are case-sensitive

The starter implementation is ugly and mostly working, but it does not yet satisfy the new feature/user validation tests.

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
