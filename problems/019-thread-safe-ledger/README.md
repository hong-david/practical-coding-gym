# 019 Thread-Safe Ledger

## Goal

Build an in-memory ledger that remains correct under concurrent access from multiple threads. This lab is separate from async work and focuses on locks, critical sections, snapshots, and avoiding deadlocks.

## Files to Implement

```txt
src/
    thread_safe_ledger.py
fixtures/
```

## API/functions/classes expected

```python
class ThreadSafeLedger:
    def create_account(self, account_id: str, initial_balance=0) -> dict: ...
    def deposit(self, account_id: str, amount) -> dict: ...
    def withdraw(self, account_id: str, amount) -> dict: ...
    def transfer(self, from_account_id: str, to_account_id: str, amount) -> dict: ...
    def get_balance(self, account_id: str): ...
    def snapshot(self) -> dict: ...
```

## Input/output shape

Balances should be exact Decimal-compatible values. Mutating operations return dictionaries describing the operation and resulting balances. `snapshot()` returns a copy of all balances and should not expose mutable internal state.

## Level 1 MVP

Support account creation, deposit, withdraw, transfer, and balance lookup.

## Level 2 Edge Cases

Handle duplicate accounts, missing accounts, invalid amounts, insufficient funds, concurrent deposits, concurrent transfers, lock ordering to avoid deadlocks, snapshot consistency, and mutation safety.

## Level 3 Senior Follow-Ups

Add per-account locks, transaction logs, stress tests, lock contention metrics, timeout-aware lock acquisition, and design notes comparing coarse-grained and fine-grained locking.

## Provided test command

```bash
./scripts/test-problem.sh 019-thread-safe-ledger provided
```

## Custom test command

```bash
./scripts/test-problem.sh 019-thread-safe-ledger custom
```

## Manual run command

```bash
python -m pytest problems/019-thread-safe-ledger/tests/provided
```

## Definition of Done

Provided tests pass, custom tests include at least one concurrent scenario, balances remain correct after stress runs, and implementation avoids deadlocks.

## PR Review Checklist

Check lock scope, deadlock risk, validation outside/inside critical sections, Decimal handling, snapshot copying, exception safety, test determinism, and whether concurrency behavior is documented.
