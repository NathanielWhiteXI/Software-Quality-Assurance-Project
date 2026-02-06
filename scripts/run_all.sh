#!/bin/bash

echo "Running all test cases..."

for input in tests/inputs/*.txt; do
    filename=$(basename "$input")
    echo "Running $filename"
    python3 src/main.py < "$input" > "tests/output_$filename"
done