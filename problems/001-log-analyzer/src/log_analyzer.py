ALLOWED_METHODS = {
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
}

def _empty_summary():
    return {
        "total_lines": 0,
        "valid_lines": 0,
        "malformed_lines": 0,
        "status_codes": {},
        "methods": {},
        "paths": {},
    }

def _process_line(line, response):
    line = line.strip()
    # skip empty lines
    if not line:
        return
    response["total_lines"] += 1
    # collapse ws runs
    parsed = _parse_line(line.split())
    if parsed is None:
        response["malformed_lines"] += 1
        return
    response["valid_lines"] += 1
    response["status_codes"][parsed["status"]] = response["status_codes"].get(parsed["status"], 0) + 1
    response["methods"][parsed["method"]] = response["methods"].get(parsed["method"], 0) + 1
    response["paths"][parsed["path"]] = response["paths"].get(parsed["path"], 0) + 1

def _is_non_empty(field):
    return bool(field)

def _is_valid_method(field):
    return field in ALLOWED_METHODS

def _is_valid_path(field):
    return field.startswith("/")

def _is_valid_status(field):
    if not field.isdigit():
        return False
    status = int(field)
    return 100 <= status <= 599

def _is_valid_duration(field):
    return field.endswith('ms') and field[:-2].isdigit()

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
        "status": int(status_text)
    }

def analyze_log_text(text):
    response = _empty_summary()
    for line in text.splitlines():
        _process_line(line, response)
    return response
        

def analyze_log_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return analyze_log_text(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f'File not Found: {filepath}')
