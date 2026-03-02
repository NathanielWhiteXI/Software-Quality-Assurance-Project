#!/bin/bash
fail=0

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXPECTED_DIR="$PROJECT_ROOT/tests/expected_txt"
OUTPUT_DIR="$PROJECT_ROOT/outputs"

echo "Checking test results..."

for expected in "$EXPECTED_DIR"/*.txt; do
  base=$(basename "$expected")
  diff "$OUTPUT_DIR/$base" "$expected" || { echo "$base: FAIL"; fail=1; }
done

exit $fail