#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source "$case_dir/source/container.env"
exec "$case_dir/../harness/run-container.sh" "$case_dir" "$@"
