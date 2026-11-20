#!/bin/bash
set -euo pipefail
case_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export DP_IMAGE=dp-kindle:1
export DP_EXTRA_APT='pandoc=2.17.1.1-2~deb12u1 epubcheck=4.2.6-2'
export DP_EXTRA_PIP='playwright==1.51.0 lxml==5.3.1'
exec "$case_dir/../harness/run-container.sh" "$case_dir" "$@"
