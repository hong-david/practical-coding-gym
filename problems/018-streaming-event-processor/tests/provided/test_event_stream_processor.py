from decimal import Decimal
from pathlib import Path
import json
import sys

import pytest

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROBLEM_ROOT / "src"
FIXTURES_DIR = PROBLEM_ROOT / "fixtures"
sys.path.insert(0, str(SRC_DIR))

from event_stream_processor import iter_events, parse_event_line, summarize_event_stream, write_summary


VALID_LINE = '{"event_id":"e1","timestamp":"2026-05-01T10:00:00Z","user_id":"u1","event_type":"view","value":"1.50"}'


def test_parse_event_line_returns_dict():
    assert parse_event_line(VALID_LINE)["event_id"] == "e1"


def test_parse_event_line_trims_whitespace():
    assert parse_event_line(f"  {VALID_LINE}  ")["event_type"] == "view"


def test_parse_event_line_rejects_malformed_json():
    with pytest.raises(ValueError):
        parse_event_line("not-json")


@pytest.mark.parametrize("field", ["event_id", "timestamp", "user_id", "event_type"])
def test_parse_event_line_requires_core_fields(field):
    event = json.loads(VALID_LINE)
    event.pop(field)
    with pytest.raises(ValueError):
        parse_event_line(json.dumps(event))


def test_blank_lines_are_ignored_by_iterator():
    assert list(iter_events(["", "   ", VALID_LINE])) == [parse_event_line(VALID_LINE)]


def test_iter_events_is_lazy():
    consumed = []

    def lines():
        consumed.append("first")
        yield VALID_LINE
        consumed.append("second")
        yield "not-json"

    iterator = iter_events(lines())
    assert consumed == []
    next(iterator)
    assert consumed == ["first"]


def test_iter_events_can_skip_malformed_when_configured_by_summary():
    result = summarize_event_stream([VALID_LINE, "not-json"])
    assert result["malformed_lines"] == 1


def test_summary_counts_total_non_blank_lines():
    result = summarize_event_stream(["", VALID_LINE, "not-json"])
    assert result["total_lines"] == 2


def test_summary_counts_valid_lines():
    assert summarize_event_stream([VALID_LINE])["valid_lines"] == 1


def test_summary_counts_event_types():
    assert summarize_event_stream([VALID_LINE])["event_types"] == {"view": 1}


def test_summary_counts_users():
    assert summarize_event_stream([VALID_LINE])["users"] == {"u1": 1}


def test_summary_sums_purchase_revenue_as_decimal():
    line = '{"event_id":"e2","timestamp":"2026-05-01T10:00:00Z","user_id":"u1","event_type":"purchase","value":"12.50"}'
    assert summarize_event_stream([line])["revenue"] == Decimal("12.50")


def test_non_purchase_value_does_not_increase_revenue():
    assert summarize_event_stream([VALID_LINE])["revenue"] == Decimal("0.00")


def test_duplicate_event_ids_are_reported():
    result = summarize_event_stream([VALID_LINE, VALID_LINE])
    assert result["duplicate_event_ids"] == ["e1"]


def test_duplicate_events_count_as_valid_but_not_double_revenue():
    line = '{"event_id":"e2","timestamp":"2026-05-01T10:00:00Z","user_id":"u1","event_type":"purchase","value":"12.50"}'
    result = summarize_event_stream([line, line])
    assert result["valid_lines"] == 2
    assert result["revenue"] == Decimal("12.50")


def test_summary_handles_empty_stream():
    result = summarize_event_stream([])
    assert result["total_lines"] == 0
    assert result["event_types"] == {}


def test_summary_emits_checkpoints():
    lines = [VALID_LINE, VALID_LINE, VALID_LINE]
    result = summarize_event_stream(lines, checkpoint_every=2)
    assert result["checkpoints"] == [2]


def test_checkpoint_interval_must_be_positive():
    with pytest.raises(ValueError):
        summarize_event_stream([VALID_LINE], checkpoint_every=0)


def test_write_summary_writes_json_file(tmp_path):
    input_path = FIXTURES_DIR / "small_events.ndjson"
    output_path = tmp_path / "summary.json"
    write_summary(input_path, output_path)
    assert output_path.exists()


def test_write_summary_returns_same_summary_it_writes(tmp_path):
    output_path = tmp_path / "summary.json"
    result = write_summary(FIXTURES_DIR / "small_events.ndjson", output_path)
    assert json.loads(output_path.read_text())["valid_lines"] == result["valid_lines"]


def test_write_summary_missing_input_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        write_summary(tmp_path / "missing.ndjson", tmp_path / "out.json")


def test_summary_uses_stream_without_len():
    def line_generator():
        for _ in range(3):
            yield VALID_LINE

    assert summarize_event_stream(line_generator())["total_lines"] == 3
