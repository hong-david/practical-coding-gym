from pathlib import Path
import sys
import pytest
PROBLEM_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROBLEM_ROOT / "src"
FIXTURES_DIR = PROBLEM_ROOT / "fixtures"
sys.path.insert(0, str(SRC_DIR))
from reconciler import reconcile_transactions, reconcile_transaction_files

def read(name): return (FIXTURES_DIR / name).read_text()

CASES = [
    ("perfect match", "internal_perfect.csv", "provider_perfect.csv", ("summary", "matched_count"), 2),
    ("required matched key", "internal_empty.csv", "provider_empty.csv", ("matched",), list),
    ("required missing provider key", "internal_empty.csv", "provider_empty.csv", ("missing_from_provider",), list),
    ("required missing internal key", "internal_empty.csv", "provider_empty.csv", ("missing_from_internal",), list),
    ("required mismatch key", "internal_empty.csv", "provider_empty.csv", ("amount_mismatches",), list),
    ("required duplicate internal key", "internal_empty.csv", "provider_empty.csv", ("duplicate_internal",), list),
    ("required duplicate provider key", "internal_empty.csv", "provider_empty.csv", ("duplicate_provider",), list),
    ("empty internal count", "internal_empty.csv", "provider_empty.csv", ("summary", "internal_count"), 0),
    ("empty provider count", "internal_empty.csv", "provider_empty.csv", ("summary", "provider_count"), 0),
    ("missing provider", "internal_missing_provider.csv", "provider_perfect.csv", ("summary", "missing_from_provider_count"), 1),
    ("missing internal", "internal_perfect.csv", "provider_missing_internal.csv", ("summary", "missing_from_internal_count"), 1),
    ("amount mismatch", "internal_amount_mismatch.csv", "provider_amount_mismatch.csv", ("summary", "amount_mismatch_count"), 1),
    ("duplicate internal", "internal_duplicates.csv", "provider_perfect.csv", ("summary", "duplicate_internal_count"), 1),
    ("duplicate provider", "internal_perfect.csv", "provider_duplicates.csv", ("summary", "duplicate_provider_count"), 1),
    ("normalization", "internal_normalized.csv", "provider_normalized.csv", ("summary", "matched_count"), 1),
    ("malformed internal", "internal_malformed.csv", "provider_perfect.csv", ("summary", "malformed_internal_count"), 1),
    ("malformed provider", "internal_perfect.csv", "provider_malformed.csv", ("summary", "malformed_provider_count"), 1),
]
@pytest.mark.parametrize("label,internal,provider,path,expected", CASES)
def test_reconcile_cases(label, internal, provider, path, expected):
    result = reconcile_transactions(read(internal), read(provider))
    value = result
    for key in path: value = value[key]
    assert isinstance(value, expected) if isinstance(expected, type) else value == expected

def test_currency_is_case_insensitive():
    result = reconcile_transactions("transaction_id,date,amount,currency,description\na,2026-01-01,1.00,usd,Coffee\n", "provider_id,date,amount,currency,description\nb,2026-01-01,1.00,USD,coffee\n")
    assert result["summary"]["matched_count"] == 1

def test_amounts_compare_as_decimals():
    result = reconcile_transactions("transaction_id,date,amount,currency,description\na,2026-01-01,1.10,USD,Coffee\n", "provider_id,date,amount,currency,description\nb,2026-01-01,1.1,USD,coffee\n")
    assert result["summary"]["matched_count"] == 1

def test_empty_lines_are_ignored():
    result = reconcile_transactions("transaction_id,date,amount,currency,description\n\na,2026-01-01,1.00,USD,Coffee\n\n", "provider_id,date,amount,currency,description\nb,2026-01-01,1.00,USD,coffee\n")
    assert result["summary"]["internal_count"] == 1

def test_file_function_reads_two_files():
    assert reconcile_transaction_files(FIXTURES_DIR / "internal_perfect.csv", FIXTURES_DIR / "provider_perfect.csv")["summary"]["matched_count"] == 2

def test_missing_internal_file_raises_clear_error():
    with pytest.raises(FileNotFoundError, match="missing_internal.csv"):
        reconcile_transaction_files(FIXTURES_DIR / "missing_internal.csv", FIXTURES_DIR / "provider_perfect.csv")

def test_missing_provider_file_raises_clear_error():
    with pytest.raises(FileNotFoundError, match="missing_provider.csv"):
        reconcile_transaction_files(FIXTURES_DIR / "internal_perfect.csv", FIXTURES_DIR / "missing_provider.csv")
