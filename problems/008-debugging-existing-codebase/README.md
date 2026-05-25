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

Orders are dictionaries:

```python
{
    "items": [
        {"sku": "sku-1", "quantity": 2, "unit_price": 10.00},
    ],
    "discount": 2,  # optional fixed amount
}
```

Percentage discounts are represented as:

```python
{"discount": {"type": "percent", "value": 10}}
```

Inventory maps SKU strings to available quantities:

```python
{
    "sku-1": 5,
    "sku-2": 0,
}
```

`process_order(order, inventory)` returns:

```python
{
    "subtotal": 20.00,
    "tax": 2.00,
    "total": 22.00,
}
```

and decrements inventory by each ordered quantity only if the full order succeeds.

`refund_order(order, inventory)` returns `True` and restores inventory by each item quantity.

Expected errors:

- missing `items` raises `ValueError`
- missing or insufficient inventory raises `ValueError`
- non-positive quantity raises `ValueError`
- negative prices raise `ValueError`
- refunding an unknown SKU raises `KeyError`

Money values should be rounded to two decimal places. The starter implementation intentionally violates several of these rules.

Example expected behavior:

```python
inventory = {"sku-1": 5}
order = {
    "items": [
        {"sku": "sku-1", "quantity": 3, "unit_price": 10.00},
    ],
    "discount": {"type": "percent", "value": 10},
}

process_order(order, inventory) == {
    "subtotal": 27.00,
    "tax": 2.70,
    "total": 29.70,
}

inventory == {"sku-1": 2}

refund_order(order, inventory) is True
inventory == {"sku-1": 5}
```

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
