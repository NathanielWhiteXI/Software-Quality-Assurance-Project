#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="$PROJECT_ROOT/tests/inputs"
ACCOUNTS_FILE="$PROJECT_ROOT/tests/current_accounts/currentaccounts.txt"
OUTPUT_DIR="$PROJECT_ROOT/outputs"
SRC_MAIN="$PROJECT_ROOT/src/main.py"

mkdir -p "$OUTPUT_DIR"

echo "Running all test inputs..."
echo "--------------------------------"

find "$INPUT_DIR" -name "*.txt" -print0 | while IFS= read -r -d '' input_file
do
    base=$(basename "$input_file" .txt)

    echo "Running $base"
    echo "--------------------------------"

    py "$SRC_MAIN" "$ACCOUNTS_FILE" "$OUTPUT_DIR/$base.atf" \
        < "$input_file" > "$OUTPUT_DIR/$base.out"

    echo ""
done

echo "Finished running all tests."