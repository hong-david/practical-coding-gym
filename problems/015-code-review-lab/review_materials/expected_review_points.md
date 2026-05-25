# Expected Review Points

A strong review should mention:

- The function mutates input orders by adding `total`.
- Cancelled orders are included in `count`.
- Missing validation hides malformed data.
- Float money arithmetic can cause rounding issues.
- Unknown customers are silently grouped under `unknown`.
- Negative quantity and price behavior is undefined.
- Tests should cover empty input, cancelled orders, malformed rows, mutation safety, and money precision.
- Request changes rather than approve until correctness and tests improve.
