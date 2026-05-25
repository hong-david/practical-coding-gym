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

Both APIs return the same compact reconciliation report:

```python
{
    "matched": [
        {"transaction_id": "int-1", "provider_id": "prov-1"},
    ],
    "missing_from_provider": [
        {
            "transaction_id": "int-2",
            "date": "2026-05-02",
            "amount": "9.99",
            "currency": "USD",
            "description": "snack",
        },
    ],
    "missing_from_internal": [
        {
            "provider_id": "prov-5",
            "date": "2026-05-04",
            "amount": "20.00",
            "currency": "USD",
            "description": "gym",
        },
    ],
    "amount_mismatches": [
        {
            "transaction_id": "int-3",
            "provider_id": "prov-3",
            "date": "2026-05-03",
            "currency": "USD",
            "description": "taxi",
            "internal_amount": "10.00",
            "provider_amount": "11.00",
        },
    ],
    "duplicate_internal": [
        {"transaction_id": "int-4", "duplicate_of": "int-1"},
    ],
    "duplicate_provider": [
        {"provider_id": "prov-4", "duplicate_of": "prov-1"},
    ],
    "malformed_internal": [
        {"line_number": 6, "raw": "bad,row"},
    ],
    "malformed_provider": [
        {"line_number": 6, "raw": "also,bad"},
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

Keep list entries small. Include source IDs and the fields needed to explain the result; do not build a deeply nested audit report for the baseline interview solution. It is fine to include extra diagnostic fields such as `line_number` or `error`, but the provided tests only require the buckets and counts. Use string amounts in returned dictionaries to avoid exposing binary floating-point artifacts. Internally, compare amounts with `Decimal`.

Counting rules:

- `internal_count` and `provider_count` count parsed, non-malformed transaction rows, including duplicates.
- blank lines do not count as parsed or malformed rows.
- malformed rows count only in `malformed_internal_count` or `malformed_provider_count`.
- duplicates are still included in `internal_count` or `provider_count`.
- duplicate rows should also appear in the relevant duplicate list.
- the first occurrence of a duplicated normalized transaction remains eligible for matching; later duplicates go in the duplicate list and should not also be reported as matched, missing, or mismatched.

For amount mismatches, compare records by normalized date, currency, and description when no exact amount match exists. Put those records in `amount_mismatches`, not in both missing buckets.

`reconcile_transactions(...)` parses and reconciles CSV text directly.

`reconcile_transaction_files(...)` reads both files, raises a clear `FileNotFoundError` if either path is missing, and otherwise returns the same dictionary shape as `reconcile_transactions(...)`.

The provided tests require the top-level keys and summary counts above. The exact fields inside list entries can be richer, but they should include enough source record detail to debug why each row landed in that bucket.

Example mixed reconciliation:

```python
internal_csv = """transaction_id,date,amount,currency,description
int-1,2026-05-01,10.00,USD,Coffee
int-2,2026-05-02,9.99,USD,Snack
int-3,2026-05-03,12.00,USD,Taxi
int-4,2026-05-01,10.00,USD,Coffee
bad,row
"""

provider_csv = """provider_id,date,amount,currency,description
prov-1,2026-05-01,10.00,USD,Coffee
prov-3,2026-05-03,13.00,USD,Taxi
prov-5,2026-05-04,20.00,USD,Gym
prov-4,2026-05-01,10.00,USD,Coffee
also,bad
"""

reconcile_transactions(internal_csv, provider_csv) == {
    "matched": [
        {"transaction_id": "int-1", "provider_id": "prov-1"},
    ],
    "missing_from_provider": [
        {
            "transaction_id": "int-2",
            "date": "2026-05-02",
            "amount": "9.99",
            "currency": "USD",
            "description": "snack",
        },
    ],
    "missing_from_internal": [
        {
            "provider_id": "prov-5",
            "date": "2026-05-04",
            "amount": "20.00",
            "currency": "USD",
            "description": "gym",
        },
    ],
    "amount_mismatches": [
        {
            "transaction_id": "int-3",
            "provider_id": "prov-3",
            "date": "2026-05-03",
            "currency": "USD",
            "description": "taxi",
            "internal_amount": "12.00",
            "provider_amount": "13.00",
        },
    ],
    "duplicate_internal": [
        {
            "transaction_id": "int-4",
            "duplicate_of": "int-1",
        },
    ],
    "duplicate_provider": [
        {
            "provider_id": "prov-4",
            "duplicate_of": "prov-1",
        },
    ],
    "malformed_internal": [
        {"line_number": 6, "raw": "bad,row"},
    ],
    "malformed_provider": [
        {"line_number": 6, "raw": "also,bad"},
    ],
    "summary": {
        "internal_count": 4,
        "provider_count": 4,
        "matched_count": 1,
        "missing_from_provider_count": 1,
        "missing_from_internal_count": 1,
        "amount_mismatch_count": 1,
        "duplicate_internal_count": 1,
        "duplicate_provider_count": 1,
        "malformed_internal_count": 1,
        "malformed_provider_count": 1,
    },
}
```

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
