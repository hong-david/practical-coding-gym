# 002 CSV Transaction Reconciler

## Goal

Build a CLI/library that compares internal transaction CSVs against provider/bank transaction CSVs and reports matched, unmatched, duplicate, mismatched, and malformed records.

## Files to Implement

```txt
src/
    reconciler.py
    main.py
```

## API/functions/classes expected

```python
reconcile_transactions(internal_csv_text: str, provider_csv_text: str) -> dict
reconcile_transaction_files(internal_filepath: str, provider_filepath: str) -> dict
```

## Input/output shape

Internal CSV fields:

```txt
transaction_id,date,amount,currency,description
```

Provider CSV fields:

```txt
provider_id,date,amount,currency,description
```

Both APIs return the same result shape:

```python
{
    "matched": [
        {
            "internal": {...},
            "provider": {...},
        },
    ],
    "missing_from_provider": [
        {"transaction_id": "int-2", ...},
    ],
    "missing_from_internal": [
        {"provider_id": "prov-3", ...},
    ],
    "amount_mismatches": [
        {
            "internal": {...},
            "provider": {...},
            "internal_amount": "10.00",
            "provider_amount": "11.00",
        },
    ],
    "duplicate_internal": [
        {"transaction_id": "int-2", ...},
    ],
    "duplicate_provider": [
        {"provider_id": "prov-2", ...},
    ],
    "malformed_internal": [
        {"line_number": 3, "raw": "bad,row", "error": "..."},
    ],
    "malformed_provider": [
        {"line_number": 3, "raw": "bad,row", "error": "..."},
    ],
    "summary": {
        "internal_count": 0,
        "provider_count": 0,
        "matched_count": 0,
        "missing_from_provider_count": 0,
        "missing_from_internal_count": 0,
        "amount_mismatch_count": 0,
        "duplicate_internal_count": 0,
        "duplicate_provider_count": 0,
        "malformed_internal_count": 0,
        "malformed_provider_count": 0,
    },
}
```

`reconcile_transactions(...)` parses and reconciles CSV text directly.

`reconcile_transaction_files(...)` reads both files, raises a clear `FileNotFoundError` if either path is missing, and otherwise returns the same dictionary shape as `reconcile_transactions(...)`.

The provided tests require the top-level keys and summary counts above. The exact fields inside list entries can be richer, but they should include enough source record detail to debug why each row landed in that bucket.

## Level 1 MVP

Parse CSV text, normalize fields, compare records, and return the required shape.

## Level 2 Edge Cases

Trim whitespace, compare Decimal amounts, normalize description whitespace/case, normalize currency case, ignore empty lines, detect duplicates, report malformed rows, and raise clear FileNotFoundError.

## Level 3 Senior Follow-Ups

Add JSON CLI output, configurable matching keys, date tolerance, streaming large files, and detailed audit reports.

## Provided test command

```bash
./scripts/test-problem.sh 002-csv-transaction-reconciler provided
```

## Custom test command

```bash
./scripts/test-problem.sh 002-csv-transaction-reconciler custom
```

## Manual run command

```bash
python problems/002-csv-transaction-reconciler/src/main.py problems/002-csv-transaction-reconciler/fixtures/internal_perfect.csv problems/002-csv-transaction-reconciler/fixtures/provider_perfect.csv
```

## Definition of Done

Provided tests pass, meaningful custom tests pass, manual runs work where applicable, expected errors are clear, and implementation remains focused.

## PR Review Checklist

Check correctness, edge cases, validation, error handling, source organization, mutation safety, test quality, usability, and simplicity.
