from decimal import Decimal
from pathlib import Path
import sqlite3
import sys

import pytest

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROBLEM_ROOT / "src"
MIGRATIONS_DIR = PROBLEM_ROOT / "migrations"
sys.path.insert(0, str(SRC_DIR))

from ledger import LedgerService, MigrationError, apply_migrations, initialize_database


def db_path(tmp_path):
    return tmp_path / "ledger.sqlite3"


def service(tmp_path):
    path = db_path(tmp_path)
    initialize_database(path)
    return LedgerService(path)


def test_initialize_database_creates_sqlite_file(tmp_path):
    path = db_path(tmp_path)
    initialize_database(path)
    assert path.exists()


def test_apply_migrations_creates_schema_migrations_table(tmp_path):
    path = db_path(tmp_path)
    apply_migrations(path, MIGRATIONS_DIR)
    with sqlite3.connect(path) as conn:
        tables = {row[0] for row in conn.execute("select name from sqlite_master where type='table'")}
    assert "schema_migrations" in tables


def test_apply_migrations_is_idempotent(tmp_path):
    path = db_path(tmp_path)
    apply_migrations(path, MIGRATIONS_DIR)
    apply_migrations(path, MIGRATIONS_DIR)
    with sqlite3.connect(path) as conn:
        count = conn.execute("select count(*) from schema_migrations").fetchone()[0]
    assert count == 2


def test_missing_migrations_directory_fails_clearly(tmp_path):
    with pytest.raises(FileNotFoundError):
        apply_migrations(db_path(tmp_path), tmp_path / "missing")


def test_failed_migration_rolls_back(tmp_path):
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "001_ok.sql").write_text("create table ok_table(id integer primary key);\n")
    (migrations / "002_bad.sql").write_text("create table broken(\n")
    with pytest.raises(MigrationError):
        apply_migrations(db_path(tmp_path), migrations)


def test_create_account_returns_shape(tmp_path):
    account = service(tmp_path).create_account("Cash", "usd")
    assert set(account) >= {"id", "name", "currency", "balance", "created_at", "updated_at"}


def test_create_account_trims_name(tmp_path):
    assert service(tmp_path).create_account("  Cash  ", "USD")["name"] == "Cash"


def test_create_account_normalizes_currency(tmp_path):
    assert service(tmp_path).create_account("Cash", "usd")["currency"] == "USD"


def test_blank_account_name_rejected(tmp_path):
    with pytest.raises(ValueError):
        service(tmp_path).create_account(" ", "USD")


def test_blank_currency_rejected(tmp_path):
    with pytest.raises(ValueError):
        service(tmp_path).create_account("Cash", " ")


def test_duplicate_account_name_currency_rejected(tmp_path):
    ledger = service(tmp_path)
    ledger.create_account("Cash", "USD")
    with pytest.raises(ValueError):
        ledger.create_account("Cash", "usd")


def test_get_account_returns_persisted_account(tmp_path):
    ledger = service(tmp_path)
    created = ledger.create_account("Cash", "USD")
    assert ledger.get_account(created["id"])["name"] == "Cash"


def test_get_missing_account_raises_key_error(tmp_path):
    with pytest.raises(KeyError):
        service(tmp_path).get_account(999)


def test_list_accounts_returns_creation_order(tmp_path):
    ledger = service(tmp_path)
    ledger.create_account("A", "USD")
    ledger.create_account("B", "USD")
    assert [account["name"] for account in ledger.list_accounts()] == ["A", "B"]


def test_transfer_moves_decimal_amount_atomically(tmp_path):
    ledger = service(tmp_path)
    source = ledger.create_account("Source", "USD")
    target = ledger.create_account("Target", "USD")
    ledger.record_transfer(source["id"], target["id"], Decimal("10.25"), "tx-1")
    assert ledger.get_balance(source["id"]) == Decimal("-10.25")
    assert ledger.get_balance(target["id"]) == Decimal("10.25")


def test_transfer_rejects_zero_amount(tmp_path):
    ledger = service(tmp_path)
    a = ledger.create_account("A", "USD")
    b = ledger.create_account("B", "USD")
    with pytest.raises(ValueError):
        ledger.record_transfer(a["id"], b["id"], Decimal("0"), "tx-1")


def test_transfer_rejects_negative_amount(tmp_path):
    ledger = service(tmp_path)
    a = ledger.create_account("A", "USD")
    b = ledger.create_account("B", "USD")
    with pytest.raises(ValueError):
        ledger.record_transfer(a["id"], b["id"], Decimal("-1"), "tx-1")


def test_transfer_rejects_same_account(tmp_path):
    ledger = service(tmp_path)
    account = ledger.create_account("A", "USD")
    with pytest.raises(ValueError):
        ledger.record_transfer(account["id"], account["id"], Decimal("1"), "tx-1")


def test_transfer_rejects_missing_destination_without_partial_write(tmp_path):
    ledger = service(tmp_path)
    source = ledger.create_account("Source", "USD")
    with pytest.raises(KeyError):
        ledger.record_transfer(source["id"], 999, Decimal("1.00"), "tx-1")
    assert ledger.get_balance(source["id"]) == Decimal("0.00")


def test_transfer_idempotency_key_returns_existing_transfer(tmp_path):
    ledger = service(tmp_path)
    a = ledger.create_account("A", "USD")
    b = ledger.create_account("B", "USD")
    first = ledger.record_transfer(a["id"], b["id"], Decimal("1.00"), "tx-1")
    second = ledger.record_transfer(a["id"], b["id"], Decimal("1.00"), "tx-1")
    assert second["id"] == first["id"]


def test_idempotency_key_conflict_rejected(tmp_path):
    ledger = service(tmp_path)
    a = ledger.create_account("A", "USD")
    b = ledger.create_account("B", "USD")
    ledger.record_transfer(a["id"], b["id"], Decimal("1.00"), "tx-1")
    with pytest.raises(ValueError):
        ledger.record_transfer(a["id"], b["id"], Decimal("2.00"), "tx-1")


def test_list_transactions_can_filter_by_account(tmp_path):
    ledger = service(tmp_path)
    a = ledger.create_account("A", "USD")
    b = ledger.create_account("B", "USD")
    ledger.record_transfer(a["id"], b["id"], Decimal("1.00"), "tx-1")
    assert len(ledger.list_transactions(account_id=a["id"])) == 1


def test_data_persists_across_service_instances(tmp_path):
    path = db_path(tmp_path)
    initialize_database(path)
    first = LedgerService(path)
    account = first.create_account("Cash", "USD")
    second = LedgerService(path)
    assert second.get_account(account["id"])["name"] == "Cash"
