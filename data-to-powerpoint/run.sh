#!/bin/bash
set -euo pipefail
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export DP_IMAGE=dp-deck:1
export DP_EXTRA_APT='libreoffice-impress=4:7.4.7-1+deb12u14'
export DP_EXTRA_PIP='python-pptx==1.0.2 XlsxWriter==3.3.1 lxml==6.1.3 typing-extensions==4.16.0'
exec "$here/../harness/run-container.sh" "$here" "$@"
