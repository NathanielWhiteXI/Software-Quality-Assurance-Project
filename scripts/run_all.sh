#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="$PROJECT_ROOT/tests/inputs"
SRC_MAIN="$PROJECT_ROOT/src/main.py"

echo "Running all test inputs..."
echo "----------------------------------"

find "$INPUT_DIR" -name "*.txt" -print0 | while IFS= read -r -d '' input_file
do
    test_name="$(basename "$input_file")"

    echo "Running $test_name"
    echo "----------------------------------"

    python3 "$SRC_MAIN" < "$input_file"

    echo ""
done

echo "Finished running all tests."