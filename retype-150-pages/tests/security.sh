#!/bin/bash
set -euo pipefail
case_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
source "$case_dir/source/container.env"
mkdir -p "$case_dir/proof"
uid_args=()
if ! docker info --format '{{json .SecurityOptions}}' | grep -q rootless; then
  echo 'This acquisition check runs as container root; proof files are made readable on exit.'
fi
timeout 900 docker run --rm --cpus 2 --memory 2g \
  --mount "type=bind,src=$case_dir,dst=/candidate,readonly" \
  --mount "type=bind,src=$case_dir/proof,dst=/proof" \
  "$DP_IMAGE" bash -c '
set -euo pipefail
timeout 180 apt-get update >/proof/antivirus-acquisition.log 2>&1
timeout 300 apt-get install -y --no-install-recommends clamav=1.4.3+dfsg-1~deb12u2 clamav-freshclam=1.4.3+dfsg-1~deb12u2 >>/proof/antivirus-acquisition.log 2>&1
mkdir -p /tmp/clamdb
printf "%s\n" "DatabaseDirectory /tmp/clamdb" "DatabaseOwner root" "DatabaseMirror database.clamav.net" "ConnectTimeout 15" "ReceiveTimeout 60" "MaxAttempts 2" > /tmp/freshclam.conf
if ! timeout 240 freshclam --stdout --config-file=/tmp/freshclam.conf >/proof/antivirus-update.log 2>&1; then
  echo "FAIL: antivirus definitions could not be acquired" > /proof/antivirus.log
  exit 1
fi
clamscan --database=/tmp/clamdb --version > /proof/antivirus.log
set +e
timeout 300 clamscan --database=/tmp/clamdb --recursive --infected --scan-archive=yes --max-filesize=100M --max-scansize=300M --exclude-dir="/candidate/generated" --exclude="/candidate/proof/antivirus" --exclude="/candidate/proof/publication[.]json" /candidate >> /proof/antivirus.log 2>&1
result=$?
set -e
printf "Scanner exit code: %s\n" "$result" >> /proof/antivirus.log
chmod a+r /proof/antivirus*.log
exit "$result"
'
