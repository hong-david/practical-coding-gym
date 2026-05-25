# 016 SQL Ledger Service

## Goal

Build a persistent ledger service backed by SQLite. This lab focuses on schema design, migrations, transaction boundaries, idempotency, and correctness under failure.

## Files to Implement

```txt
src/
    ledger.py
migrations/
    001_initial.sql
    002_idempotency_keys.sql
fixtures/
```

## API/functions/classes expected

```python
apply_migrations(db_path, migrations_dir) -> None
initialize_database(db_path) -> None

class LedgerService:
    def __init__(self, db_path): ...
    def create_account(self, name: str, currency: str) -> dict: ...
    def get_account(self, account_id: int) -> dict: ...
    def list_accounts(self) -> list[dict]: ...
    def record_transfer(self, from_account_id: int, to_account_id: int, amount, idempotency_key: str) -> dict: ...
    def get_balance(self, account_id: int): ...
    def list_transactions(self, account_id: int | None = None) -> list[dict]: ...
```

## Input/output shape

Accounts include `id`, `name`, `currency`, `balance`, `created_at`, and `updated_at`. Transfers include `id`, account IDs, decimal amount, idempotency key, and timestamp. Balances must be stored and compared as exact decimal values, not floats.

## Level 1 MVP

Create the SQLite schema, run migrations once, create accounts, list accounts, and return balances.

## Level 2 Edge Cases

Handle migration idempotency, ordered migration application, failed migration rollback, duplicate account names per currency, blank input, currency normalization, missing accounts, insufficient funds, exact Decimal math, and idempotent transfer retries.

## Level 3 Senior Follow-Ups

Add isolation-level notes, audit tables, optimistic locking, reconciliation exports, backfill migrations, and a CLI for migration status.

## Provided test command

```bash
./scripts/test-problem.sh 016-sql-ledger-service provided
```

## Custom test command

```bash
./scripts/test-problem.sh 016-sql-ledger-service custom
```

## Manual run command

```bash
python -m pytest problems/016-sql-ledger-service/tests/provided
```

## Definition of Done

Provided tests pass, meaningful custom tests pass, SQLite files persist data across service instances, and transfer behavior is atomic and idempotent.

## PR Review Checklist

Check migration safety, transaction boundaries, exact money handling, rollback behavior, idempotency semantics, account validation, SQL injection risk, test isolation, and whether persistence concerns are separated from business rules.
