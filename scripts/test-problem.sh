#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Usage: ./scripts/test-problem.sh <problem-folder> [provided|custom]"
  echo "Examples:"
  echo "  ./scripts/test-problem.sh 001-log-analyzer"
  echo "  ./scripts/test-problem.sh 001-log-analyzer provided"
  echo "  ./scripts/test-problem.sh 001-log-analyzer custom"
  exit 1
fi

PROBLEM="$1"
SECTION="${2:-}"

PROBLEM_DIR="problems/$PROBLEM"

if [ ! -d "$PROBLEM_DIR" ]; then
  echo "Problem directory not found: $PROBLEM_DIR"
  exit 1
fi

if [ -z "$SECTION" ]; then
  python -m pytest "$PROBLEM_DIR/tests"
else
  python -m pytest "$PROBLEM_DIR/tests/$SECTION"
fi
