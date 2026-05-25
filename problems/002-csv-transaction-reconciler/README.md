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

Internal fields: transaction_id,date,amount,currency,description. Provider fields: provider_id,date,amount,currency,description. Return matched, missing_from_provider, missing_from_internal, amount_mismatches, duplicate_internal, duplicate_provider, optional malformed sections, and summary counts.

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
