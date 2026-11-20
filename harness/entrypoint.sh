#!/bin/bash
set -euo pipefail
mkdir -p "$HOME"
profile=$(mktemp -d /tmp/lo-profile.XXXXXX)
export LO_PROFILE_URI="file://$profile"
trap 'rm -rf "$profile"' EXIT
if [[ $1 == check ]]; then
  python /case/tests/check.py /input /output
  python /harness/preview_check.py /case /output
else
  python /case/source/pipeline.py /input /output
fi
