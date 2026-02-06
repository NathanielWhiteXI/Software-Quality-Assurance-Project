#!/bin/bash

echo "Checking test results..."

for expected in tests/expected_txt/*.txt; do
    filename=$(basename "$expected")
    diff "tests/output_$filename" "$expected"

    if [ $? -eq 0 ]; then
        echo "$filename: PASS"
    else
        echo "$filename: FAIL"
    fi
done