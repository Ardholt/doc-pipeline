#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
exec bash "$case_dir/../harness/run-container.sh" "$case_dir" "$@"
