from decimal import Decimal
from pathlib import Path
import sys
import threading

import pytest

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROBLEM_ROOT / "src"))

from thread_safe_ledger import ThreadSafeLedger


def ledger_with_account(account_id="a", balance="0"):
    ledger = ThreadSafeLedger()
    ledger.create_account(account_id, Decimal(balance))
    return ledger


def test_create_account_sets_initial_balance():
    ledger = ledger_with_account("a", "10.00")
    assert ledger.get_balance("a") == Decimal("10.00")


def test_create_account_returns_shape():
    account = ThreadSafeLedger().create_account("a", Decimal("1.00"))
    assert set(account) >= {"account_id", "balance"}


def test_duplicate_account_rejected():
    ledger = ledger_with_account("a")
    with pytest.raises(ValueError):
        ledger.create_account("a")


def test_blank_account_id_rejected():
    with pytest.raises(ValueError):
        ThreadSafeLedger().create_account(" ")


def test_negative_initial_balance_rejected():
    with pytest.raises(ValueError):
        ThreadSafeLedger().create_account("a", Decimal("-1.00"))


def test_deposit_increases_balance():
    ledger = ledger_with_account("a", "1.00")
    ledger.deposit("a", Decimal("2.50"))
    assert ledger.get_balance("a") == Decimal("3.50")


def test_withdraw_decreases_balance():
    ledger = ledger_with_account("a", "5.00")
    ledger.withdraw("a", Decimal("2.00"))
    assert ledger.get_balance("a") == Decimal("3.00")


def test_withdraw_rejects_insufficient_funds():
    with pytest.raises(ValueError):
        ledger_with_account("a", "1.00").withdraw("a", Decimal("2.00"))


@pytest.mark.parametrize("method", ["deposit", "withdraw"])
def test_mutations_reject_zero_amount(method):
    ledger = ledger_with_account("a", "10.00")
    with pytest.raises(ValueError):
        getattr(ledger, method)("a", Decimal("0.00"))


@pytest.mark.parametrize("method", ["deposit", "withdraw"])
def test_mutations_reject_negative_amount(method):
    ledger = ledger_with_account("a", "10.00")
    with pytest.raises(ValueError):
        getattr(ledger, method)("a", Decimal("-1.00"))


def test_missing_account_balance_raises():
    with pytest.raises(KeyError):
        ThreadSafeLedger().get_balance("missing")


def test_deposit_missing_account_raises():
    with pytest.raises(KeyError):
        ThreadSafeLedger().deposit("missing", Decimal("1.00"))


def test_transfer_moves_money_between_accounts():
    ledger = ThreadSafeLedger()
    ledger.create_account("a", Decimal("10.00"))
    ledger.create_account("b", Decimal("1.00"))
    ledger.transfer("a", "b", Decimal("3.00"))
    assert ledger.get_balance("a") == Decimal("7.00")
    assert ledger.get_balance("b") == Decimal("4.00")


def test_transfer_rejects_same_account():
    ledger = ledger_with_account("a", "10.00")
    with pytest.raises(ValueError):
        ledger.transfer("a", "a", Decimal("1.00"))


def test_transfer_missing_account_raises_without_partial_change():
    ledger = ledger_with_account("a", "10.00")
    with pytest.raises(KeyError):
        ledger.transfer("a", "missing", Decimal("1.00"))
    assert ledger.get_balance("a") == Decimal("10.00")


def test_snapshot_returns_copy():
    ledger = ledger_with_account("a", "1.00")
    snap = ledger.snapshot()
    snap["a"] = Decimal("999.00")
    assert ledger.get_balance("a") == Decimal("1.00")


def test_concurrent_deposits_are_not_lost():
    ledger = ledger_with_account("a", "0.00")
    barrier = threading.Barrier(10)

    def worker():
        barrier.wait()
        for _ in range(100):
            ledger.deposit("a", Decimal("1.00"))

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert ledger.get_balance("a") == Decimal("1000.00")


def test_concurrent_withdrawals_respect_balance():
    ledger = ledger_with_account("a", "100.00")
    successes = []
    lock = threading.Lock()

    def worker():
        try:
            ledger.withdraw("a", Decimal("1.00"))
            with lock:
                successes.append(True)
        except ValueError:
            pass

    threads = [threading.Thread(target=worker) for _ in range(150)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(successes) == 100
    assert ledger.get_balance("a") == Decimal("0.00")


def test_concurrent_opposite_transfers_do_not_deadlock():
    ledger = ThreadSafeLedger()
    ledger.create_account("a", Decimal("100.00"))
    ledger.create_account("b", Decimal("100.00"))

    def ab():
        for _ in range(100):
            ledger.transfer("a", "b", Decimal("1.00"))

    def ba():
        for _ in range(100):
            ledger.transfer("b", "a", Decimal("1.00"))

    t1 = threading.Thread(target=ab)
    t2 = threading.Thread(target=ba)
    t1.start()
    t2.start()
    t1.join(timeout=2)
    t2.join(timeout=2)
    assert not t1.is_alive()
    assert not t2.is_alive()
    assert ledger.get_balance("a") + ledger.get_balance("b") == Decimal("200.00")


def test_snapshot_is_consistent_during_concurrent_updates():
    ledger = ledger_with_account("a", "0.00")

    def worker():
        for _ in range(50):
            ledger.deposit("a", Decimal("1.00"))

    thread = threading.Thread(target=worker)
    thread.start()
    snapshot = ledger.snapshot()
    thread.join()
    assert snapshot["a"] <= ledger.get_balance("a")


def test_operation_results_are_mutation_safe():
    ledger = ledger_with_account("a", "1.00")
    result = ledger.deposit("a", Decimal("1.00"))
    result["balance"] = Decimal("999.00")
    assert ledger.get_balance("a") == Decimal("2.00")
