#!/bin/bash
set -euo pipefail
here=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
harness=$(cd "$here/../harness" && pwd)
uid_args=()
if ! docker info --format '{{json .SecurityOptions}}' | grep -q rootless; then uid_args=(--user "$(id -u):$(id -g)"); fi
timeout 600 docker run --rm --cpus 2 --memory 2g --network none \
  --read-only --tmpfs /tmp:rw,nosuid,size=768m --cap-drop ALL --security-opt no-new-privileges \
  "${uid_args[@]}" --env HOME=/tmp/home --env PYTHONDONTWRITEBYTECODE=1 \
  --env LO_PROFILE_URI=file:///tmp/acceptance-profile \
  --mount "type=bind,src=$here,dst=/case,readonly" \
  --mount "type=bind,src=$harness,dst=/harness,readonly" \
  --mount "type=bind,src=$here/output,dst=/output" \
  dp-deck:1 bash -c 'mkdir -p "$HOME"; python /case/tests/acceptance.py > /output/acceptance.json'
echo 'PASS: repeatability, paths with spaces, replacement values and pagination'
