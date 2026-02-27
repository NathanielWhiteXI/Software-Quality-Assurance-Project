#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="$PROJECT_ROOT/tests/inputs"
EXPECTED_DIR="$PROJECT_ROOT/tests/expected_txt"
SRC_MAIN="$PROJECT_ROOT/src/main.py"

PASS_COUNT=0
FAIL_COUNT=0

echo "Checking all tests..."
echo "----------------------------------"

for input_file in "$INPUT_DIR"/*.txt
do
    test_name=$(basename "$input_file")
    expected_file="$EXPECTED_DIR/$test_name"
    output_file="/tmp/output_$test_name"

    echo "Checking $test_name"

    python3 "$SRC_MAIN" < "$input_file" > "$output_file"

    if diff -q "$output_file" "$expected_file" > /dev/null
    then
        echo "PASS"
        ((PASS_COUNT++))
    else
        echo "FAIL"
        echo "Differences:"
        diff "$output_file" "$expected_file"
        ((FAIL_COUNT++))
    fi

    echo "----------------------------------"
done

echo "Total Passed: $PASS_COUNT"
echo "Total Failed: $FAIL_COUNT"

if [ $FAIL_COUNT -eq 0 ]
then
    echo "🎉 All tests passed!"
else
    echo "Some tests failed."
fi
