#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export DP_IMAGE=dp-school-forms:1
export DP_EXTRA_APT='libreoffice-writer=4:7.4.7-1+deb12u14 python3-uno=4:7.4.7-1+deb12u14'
exec "$case_dir/../harness/run-container.sh" "$case_dir" "$@"
