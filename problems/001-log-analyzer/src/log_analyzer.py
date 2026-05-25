ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}


def _empty_result():
    return {
        "total_lines": 0,
        "valid_lines": 0,
        "malformed_lines": 0,
        "status_codes": {},
        "methods": {},
        "paths": {},
    }


def _is_non_empty(value):
    return bool(value)


def _is_valid_method(method):
    return method in ALLOWED_METHODS


def _is_valid_path(path):
    return path.startswith("/")


def _is_valid_status(status_text):
    if not status_text.isdigit():
        return False
    status = int(status_text)
    return 100 <= status <= 599


def _is_valid_duration(duration):
    return duration.endswith("ms") and duration[:-2].isdigit()


def _parse_line(fields):
    if len(fields) != 7:
        return None

    timestamp, level, ip, method, path, status_text, duration = fields

    if not _is_non_empty(timestamp):
        return None
    if not _is_non_empty(level):
        return None
    if not _is_non_empty(ip):
        return None
    if not _is_valid_method(method):
        return None
    if not _is_valid_path(path):
        return None
    if not _is_valid_status(status_text):
        return None
    if not _is_valid_duration(duration):
        return None

    return {
        "method": method,
        "path": path,
        "status": int(status_text),
    }


def _process_line(line, result):
    line = line.strip()
    if not line:
        return

    result["total_lines"] += 1

    parsed = _parse_line(line.split())
    if parsed is None:
        result["malformed_lines"] += 1
        return

    result["valid_lines"] += 1
    result["status_codes"][parsed["status"]] = (
        result["status_codes"].get(parsed["status"], 0) + 1
    )
    result["methods"][parsed["method"]] = (
        result["methods"].get(parsed["method"], 0) + 1
    )
    result["paths"][parsed["path"]] = result["paths"].get(parsed["path"], 0) + 1


def analyze_log_text(text):
    result = _empty_result()
    for line in text.splitlines():
        _process_line(line, result)
    return result


def analyze_log_file(filepath):
    path = str(filepath)
    try:
        with open(path, "r", encoding="utf-8") as file:
            return analyze_log_text(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
