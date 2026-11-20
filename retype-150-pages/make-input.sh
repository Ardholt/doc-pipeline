#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
[[ $# == 2 && $1 == --output ]] || { echo 'Usage: ./make-input.sh --output NEW_DIRECTORY' >&2; exit 2; }
[[ ! -e $2 ]] || { echo 'ERROR: corpus destination must not exist' >&2; exit 2; }
source "$case_dir/source/container.env"
mkdir -p -- "$2"
out=$(realpath -- "$2")
harness=$(cd "$case_dir/../harness" && pwd)
timeout 1500 docker build --tag "$DP_IMAGE" --build-arg "EXTRA_APT=$DP_EXTRA_APT" --build-arg "EXTRA_PIP=$DP_EXTRA_PIP" --file "$harness/Dockerfile" "$harness"
uid_args=()
if ! docker info --format '{{json .SecurityOptions}}' | grep -q rootless; then uid_args=(--user "$(id -u):$(id -g)"); fi
timeout 900 docker run --rm --cpus 2 --memory 2g --network none --read-only --tmpfs /tmp:rw,nosuid,size=512m --cap-drop ALL --security-opt no-new-privileges "${uid_args[@]}" --env PYTHONDONTWRITEBYTECODE=1 --mount "type=bind,src=$case_dir,dst=/case,readonly" --mount "type=bind,src=$out,dst=/output" "$DP_IMAGE" python /case/source/generate.py /case/source/reference.json /output
