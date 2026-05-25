# 018 Streaming Event Processor

## Goal

Process very large newline-delimited event streams without loading the entire input into memory. This lab focuses on lazy iteration, malformed record handling, aggregation, checkpointing, and file streaming.

## Files to Implement

```txt
src/
    event_stream_processor.py
fixtures/
    small_events.ndjson
    malformed_events.ndjson
```

## API/functions/classes expected

```python
parse_event_line(line: str) -> dict
iter_events(lines) -> iterator[dict]
summarize_event_stream(lines, checkpoint_every: int | None = None) -> dict
write_summary(input_path: str, output_path: str) -> dict
```

## Input/output shape

Input is newline-delimited JSON. Each valid event has `event_id`, `timestamp`, `user_id`, `event_type`, and optional `value`. Summaries include total line counts, valid/malformed counts, counts by event type/user, revenue totals, duplicate IDs, and checkpoints when requested.

## Level 1 MVP

Parse event lines lazily, ignore blank lines, count valid events by type, and return a summary dictionary.

## Level 2 Edge Cases

Handle malformed JSON, missing fields, duplicate event IDs, blank lines, numeric values as Decimal-compatible data, generator laziness, memory-safe file reading, checkpoint intervals, and output file writing.

## Level 3 Senior Follow-Ups

Add backpressure-friendly APIs, resumable checkpoints, compressed input, partitioned output, schema versions, dead-letter files, and performance benchmarks.

## Provided test command

```bash
./scripts/test-problem.sh 018-streaming-event-processor provided
```

## Custom test command

```bash
./scripts/test-problem.sh 018-streaming-event-processor custom
```

## Manual run command

```bash
python -m pytest problems/018-streaming-event-processor/tests/provided
```

## Definition of Done

Provided tests pass, custom tests cover at least one high-volume or malformed input case, and implementation preserves streaming behavior.

## PR Review Checklist

Check laziness, malformed input handling, duplicate detection, memory growth, exact aggregation, file I/O separation, clear summary shape, and realistic behavior for partial failures.
