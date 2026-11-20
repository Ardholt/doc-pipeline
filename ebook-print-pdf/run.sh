#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export DP_IMAGE=dp-ebook:1
export DP_EXTRA_APT='pandoc=2.17.1.1-2~deb12u1 weasyprint=57.2-1 python3-bs4=4.11.2-2'
exec "$case_dir/../harness/run-container.sh" "$case_dir" "$@"
