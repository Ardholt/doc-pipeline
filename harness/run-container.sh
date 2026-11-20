#!/bin/bash
set -euo pipefail
case_dir=$1; shift
input="$case_dir/input"; output="$case_dir/output"; mode=run
while (($#)); do
  case "$1" in
    --input|--output) (($# >= 2)) || { echo "ERROR: $1 needs a directory" >&2; exit 2; }
      if [[ $1 == --input ]]; then input=$2; else output=$2; fi; shift 2 ;;
    --check) mode=check; shift ;;
    --help) echo 'run.sh [--input DIRECTORY] [--output DIRECTORY] [--check]'; exit 0 ;;
    *) echo "ERROR: unknown argument: $1" >&2; exit 2 ;;
  esac
done
[[ -d $input ]] || { echo 'ERROR: input directory does not exist' >&2; exit 2; }
input=$(realpath "$input")
output=$(realpath -m "$output")
case "$output/" in "$input/"*) echo 'ERROR: output must be separate from input' >&2; exit 2;; esac
case "$input/" in "$output/"*) echo 'ERROR: input must not be inside output' >&2; exit 2;; esac
[[ $input != *,* && $output != *,* && $case_dir != *,* ]] || { echo 'ERROR: commas in paths are not supported by Docker mounts' >&2; exit 2; }
mkdir -p "$output"
command -v docker >/dev/null || { echo 'ERROR: Docker is required' >&2; exit 2; }
image=${DP_IMAGE:-dp-base:1}
start=$SECONDS
harness=$(cd "$case_dir/../harness" && pwd)
if [[ $mode == check ]]; then
  docker image inspect "$image" >/dev/null 2>&1 || { echo "ERROR: run ./run.sh once to build dp-base:1" >&2; exit 2; }
else
  timeout 1500 docker build --tag "$image" --build-arg "EXTRA_APT=${DP_EXTRA_APT:-}" --build-arg "EXTRA_PIP=${DP_EXTRA_PIP:-}" --file "$harness/Dockerfile" "$harness"
fi
uid_args=()
if ! docker info --format '{{json .SecurityOptions}}' | grep -q rootless; then uid_args=(--user "$(id -u):$(id -g)"); fi
timeout 1080 docker run --rm --cpus 2 --memory 2g --network none \
  --read-only --tmpfs /tmp:rw,nosuid,size=768m --cap-drop ALL --security-opt no-new-privileges \
  "${uid_args[@]}" --env HOME=/tmp/home --env PYTHONDONTWRITEBYTECODE=1 \
  --mount "type=bind,src=$case_dir,dst=/case,readonly" \
  --mount "type=bind,src=$harness,dst=/harness,readonly" \
  --mount "type=bind,src=$input,dst=/input,readonly" \
  --mount "type=bind,src=$output,dst=/output" \
  "$image" bash /harness/entrypoint.sh "$mode"
echo "PASS: $mode completed; elapsed $((SECONDS-start)) seconds (including setup)"
