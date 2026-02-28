#!/bin/bash


PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="$PROJECT_ROOT/tests/inputs"
EXPECTED_DIR="$PROJECT_ROOT/tests/expected_txt"
SRC_MAIN="$PROJECT_ROOT/src/main.py"
TEMP_DIR="$PROJECT_ROOT/tests/temp_outputs"

mkdir -p "$TEMP_DIR"

PASS_COUNT=0
FAIL_COUNT=0

echo "Checking all tests..."
echo "----------------------------------"

while IFS= read -r -d '' input_file; do
    test_name="$(basename "$input_file")"
    expected_file="$EXPECTED_DIR/$test_name"
    output_file="$TEMP_DIR/$test_name"

    echo "Checking $test_name"

    python3 "$SRC_MAIN" t < "$input_file" > "$output_file"

    if [ -f "$expected_file" ]; then
        if diff -q "$output_file" "$expected_file" > /dev/null; then
            echo "PASS"
            PASS_COUNT=$((PASS_COUNT+1))
        else
            echo "FAIL"
            echo "Differences:"
            diff "$output_file" "$expected_file"
            FAIL_COUNT=$((FAIL_COUNT+1))
        fi
    else
        echo "ERROR: Expected file not found: $expected_file"
        FAIL_COUNT=$((FAIL_COUNT+1))
    fi

    echo "----------------------------------"
done < <(find "$INPUT_DIR" -name "*.txt" -print0)

echo "Total Passed: $PASS_COUNT"
echo "Total Failed: $FAIL_COUNT"

if [ "$FAIL_COUNT" -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed."
fi

read -p "Press any key to terminate."