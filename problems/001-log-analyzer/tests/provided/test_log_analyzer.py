from pathlib import Path
import sys

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROBLEM_ROOT / "src"
FIXTURES_DIR = PROBLEM_ROOT / "fixtures"

sys.path.insert(0, str(SRC_DIR))

from log_analyzer import analyze_log_text, analyze_log_file


def test_analyze_simple_log_text():
    text = """
    2026-05-24T10:15:30Z INFO 192.168.1.10 GET /api/users 200 34ms
    2026-05-24T10:15:31Z INFO 192.168.1.11 GET /api/users 200 28ms
    2026-05-24T10:15:32Z INFO 192.168.1.12 POST /login 302 45ms
    2026-05-24T10:15:33Z WARN 192.168.1.13 GET /missing 404 12ms
    2026-05-24T10:15:34Z ERROR 192.168.1.14 GET /api/orders 500 90ms
    """

    result = analyze_log_text(text)

    assert result == {
        "total_lines": 5,
        "valid_lines": 5,
        "malformed_lines": 0,
        "status_codes": {
            200: 2,
            302: 1,
            404: 1,
            500: 1,
        },
        "methods": {
            "GET": 4,
            "POST": 1,
        },
        "paths": {
            "/api/users": 2,
            "/login": 1,
            "/missing": 1,
            "/api/orders": 1,
        },
    }


def test_blank_lines_are_ignored():
    text = """


    2026-05-24T10:15:30Z INFO 192.168.1.10 GET /api/users 200 34ms


    """

    result = analyze_log_text(text)

    assert result["total_lines"] == 1
    assert result["valid_lines"] == 1
    assert result["malformed_lines"] == 0
    assert result["status_codes"] == {200: 1}
    assert result["methods"] == {"GET": 1}
    assert result["paths"] == {"/api/users": 1}


def test_empty_input_returns_empty_summary():
    result = analyze_log_text("")

    assert result == {
        "total_lines": 0,
        "valid_lines": 0,
        "malformed_lines": 0,
        "status_codes": {},
        "methods": {},
        "paths": {},
    }


def test_mixed_valid_and_invalid_lines():
    text = """
    2026-05-24T10:15:30Z INFO 192.168.1.10 GET /api/users 200 34ms
    this line is malformed
    2026-05-24T10:15:31Z INFO 192.168.1.11 GET /api/users 200 28ms
    2026-05-24T10:15:32Z INFO 192.168.1.12 POST /login not_a_status 45ms
    2026-05-24T10:15:33Z WARN 192.168.1.13 GET /missing 404 12ms
    2026-05-24T10:15:34Z ERROR 192.168.1.14 GET /api/orders 500 ninety_ms
    too many fields are present in this invalid log line
    """

    result = analyze_log_text(text)

    assert result["total_lines"] == 7
    assert result["valid_lines"] == 3
    assert result["malformed_lines"] == 4
    assert result["status_codes"] == {
        200: 2,
        404: 1,
    }
    assert result["methods"] == {
        "GET": 3,
    }
    assert result["paths"] == {
        "/api/users": 2,
        "/missing": 1,
    }


def test_extra_whitespace_between_fields_is_allowed():
    text = "   2026-05-24T10:15:30Z    INFO    192.168.1.10    GET    /api/users    200    34ms   "

    result = analyze_log_text(text)

    assert result["total_lines"] == 1
    assert result["valid_lines"] == 1
    assert result["malformed_lines"] == 0
    assert result["status_codes"] == {200: 1}
    assert result["methods"] == {"GET": 1}
    assert result["paths"] == {"/api/users": 1}


def test_unknown_http_method_is_malformed():
    text = "2026-05-24T10:15:31Z INFO 192.168.1.11 BREW /coffee 418 10ms"

    result = analyze_log_text(text)

    assert result["total_lines"] == 1
    assert result["valid_lines"] == 0
    assert result["malformed_lines"] == 1
    assert result["status_codes"] == {}
    assert result["methods"] == {}
    assert result["paths"] == {}


def test_path_must_start_with_slash():
    text = "2026-05-24T10:15:32Z INFO 192.168.1.12 GET api/no-leading-slash 200 20ms"

    result = analyze_log_text(text)

    assert result["total_lines"] == 1
    assert result["valid_lines"] == 0
    assert result["malformed_lines"] == 1


def test_status_must_be_between_100_and_599():
    text = """
    2026-05-24T10:15:33Z INFO 192.168.1.13 GET /bad-low 99 20ms
    2026-05-24T10:15:34Z INFO 192.168.1.14 GET /bad-high 600 20ms
    2026-05-24T10:15:35Z INFO 192.168.1.15 GET /good 200 20ms
    """

    result = analyze_log_text(text)

    assert result["total_lines"] == 3
    assert result["valid_lines"] == 1
    assert result["malformed_lines"] == 2
    assert result["status_codes"] == {200: 1}
    assert result["paths"] == {"/good": 1}


def test_duration_must_be_numeric_ms():
    text = """
    2026-05-24T10:15:33Z INFO 192.168.1.13 GET /bad-duration 200 20seconds
    2026-05-24T10:15:34Z INFO 192.168.1.14 GET /also-bad 200 abcms
    2026-05-24T10:15:35Z INFO 192.168.1.15 GET /good 200 20ms
    """

    result = analyze_log_text(text)

    assert result["total_lines"] == 3
    assert result["valid_lines"] == 1
    assert result["malformed_lines"] == 2
    assert result["status_codes"] == {200: 1}
    assert result["paths"] == {"/good": 1}


def test_analyze_log_file_reads_fixture():
    filepath = FIXTURES_DIR / "simple.log"

    result = analyze_log_file(filepath)

    assert result["total_lines"] == 5
    assert result["valid_lines"] == 5
    assert result["malformed_lines"] == 0
    assert result["status_codes"] == {
        200: 2,
        302: 1,
        404: 1,
        500: 1,
    }


def test_missing_file_raises_clear_file_not_found_error():
    filepath = FIXTURES_DIR / "does_not_exist.log"

    try:
        analyze_log_file(filepath)
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as error:
        message = str(error)
        assert "not found" in message.lower()
        assert "does_not_exist.log" in message
