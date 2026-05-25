# 008 Debugging Existing Codebase

## Goal

Debug and fix intentionally flawed order processing code. Starting code is intentionally wrong.

## Files to Implement

```txt
src/
    buggy_order_processor.py
```

## API/functions/classes expected

```python
process_order(order: dict, inventory: dict) -> dict
refund_order(order: dict, inventory: dict) -> bool
```

## Input/output shape

Orders contain items with sku, quantity, and unit_price. Inventory maps SKU to available quantity.

## Level 1 MVP

Read failing tests and fix the smallest set of bugs.

## Level 2 Edge Cases

Handle stock checks, quantities, invalid inputs, refunds, discounts, rounding, and mutation safety on failure.

## Level 3 Senior Follow-Ups

Refactor toward Decimal money handling, atomic inventory reservation, and clearer domain errors.

## Provided test command

```bash
./scripts/test-problem.sh 008-debugging-existing-codebase provided
```

## Custom test command

```bash
./scripts/test-problem.sh 008-debugging-existing-codebase custom
```

## Manual run command

No manual command beyond pytest is required for this library-style lab.

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, missing requirements, edge cases, error handling, data ownership, test quality, readability, and whether the implementation is appropriately simple.
