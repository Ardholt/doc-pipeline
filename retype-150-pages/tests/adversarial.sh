#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
harness=$(cd "$case_dir/../harness" && pwd)
source "$case_dir/source/container.env"
mkdir -p "$case_dir/proof"
uid_args=()
if ! docker info --format '{{json .SecurityOptions}}' | grep -q rootless; then uid_args=(--user "$(id -u):$(id -g)"); fi
timeout 600 docker run --rm --cpus 2 --memory 2g --network none --read-only --tmpfs /tmp:rw,nosuid,size=512m --cap-drop ALL --security-opt no-new-privileges "${uid_args[@]}" --env HOME=/tmp --env PYTHONDONTWRITEBYTECODE=1 --mount "type=bind,src=$case_dir,dst=/case,readonly" --mount "type=bind,src=$harness,dst=/harness,readonly" --mount "type=bind,src=$case_dir/input,dst=/input,readonly" --mount "type=bind,src=$case_dir/proof,dst=/output" "$DP_IMAGE" python /case/tests/adversarial.py
