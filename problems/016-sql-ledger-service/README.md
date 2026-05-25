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

Accounts are dictionaries with these minimum fields:

```python
{
    "id": 1,
    "name": "Cash",
    "currency": "USD",
    "balance": Decimal("0.00"),
    "created_at": "...",
    "updated_at": "...",
}
```

Transfers are dictionaries with these minimum fields:

```python
{
    "id": 1,
    "from_account_id": 1,
    "to_account_id": 2,
    "amount": Decimal("10.25"),
    "idempotency_key": "tx-1",
    "created_at": "...",
}
```

`create_account(...)` and `get_account(...)` return account dictionaries. `list_accounts()` returns accounts in creation order. `get_balance(account_id)` returns a `Decimal`. `record_transfer(...)` returns a transfer dictionary. `list_transactions(account_id=None)` returns transfer dictionaries, optionally filtered by either source or destination account.

Migration behavior:

- `initialize_database(db_path)` creates the database and applies bundled migrations
- `apply_migrations(db_path, migrations_dir)` records applied migration filenames in `schema_migrations`
- applying migrations multiple times is safe
- failed migrations raise `MigrationError`

Expected errors:

- missing migrations directory raises `FileNotFoundError`
- blank account names/currencies raise `ValueError`
- duplicate account name/currency pairs raise `ValueError`
- missing accounts raise `KeyError`
- zero/negative transfer amounts raise `ValueError`
- same-account transfers raise `ValueError`
- idempotency key conflicts raise `ValueError`

Balances must be stored and compared as exact decimal values, not floats. Failed transfers must not partially update balances.

Example expected behavior:

```python
initialize_database("ledger.sqlite3")
ledger = LedgerService("ledger.sqlite3")

source = ledger.create_account("Source", "usd")
target = ledger.create_account("Target", "USD")

transfer = ledger.record_transfer(
    source["id"],
    target["id"],
    Decimal("10.25"),
    idempotency_key="tx-1",
)

ledger.get_balance(source["id"]) == Decimal("-10.25")
ledger.get_balance(target["id"]) == Decimal("10.25")

ledger.record_transfer(source["id"], target["id"], Decimal("10.25"), "tx-1") == transfer
```

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
