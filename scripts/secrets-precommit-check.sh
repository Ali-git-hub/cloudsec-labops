#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"

echo "[+] Running CloudSec LabOps secret detector..."
python3 scripts/secrets-detect.py "$TARGET"
