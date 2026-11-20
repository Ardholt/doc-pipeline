#!/bin/bash
set -euo pipefail
case_dir=$(cd "$(dirname "$0")/.." && pwd)
test_area=$(mktemp -d "${TMPDIR:-/tmp}/pdf-repeat.XXXXXX")
trap 'rm -rf "$test_area"' EXIT
mkdir -p "$test_area/input with spaces" "$test_area/output with spaces"
cp "$case_dir/input/"* "$test_area/input with spaces/"
cp "$case_dir/output/report.json" "$test_area/first-report.json"
before=$(sha256sum "$test_area/input with spaces/input.pdf")
"$case_dir/run.sh" --input "$test_area/input with spaces" --output "$test_area/output with spaces"
cmp "$test_area/first-report.json" "$test_area/output with spaces/report.json"
cmp "$case_dir/output/fixed.pdf" "$test_area/output with spaces/fixed.pdf"
[[ $before == "$(sha256sum "$test_area/input with spaces/input.pdf")" ]]
"$case_dir/run.sh" --check --input "$test_area/input with spaces" --output "$test_area/output with spaces"
if "$case_dir/run.sh" --input "$test_area/absent" > "$test_area/missing.log" 2>&1; then exit 1; fi
grep -q 'ERROR: input directory does not exist' "$test_area/missing.log"
if "$case_dir/run.sh" --input "$test_area/input with spaces" --output "$test_area/input with spaces/nested" > "$test_area/nested.log" 2>&1; then exit 1; fi
[[ ! -e "$test_area/input with spaces/nested" ]]
echo 'PASS: repeat produced identical PDF bytes and report facts'
echo 'PASS: absolute paths with spaces and read-only input hashes'
echo 'PASS: missing input and overlapping paths rejected without modifying input'
