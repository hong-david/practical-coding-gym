def parse_event_line(line: str) -> dict:
    raise NotImplementedError


def iter_events(lines):
    raise NotImplementedError


def summarize_event_stream(lines, checkpoint_every=None) -> dict:
    raise NotImplementedError


def write_summary(input_path: str, output_path: str) -> dict:
    raise NotImplementedError
