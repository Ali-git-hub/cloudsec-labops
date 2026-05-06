#!/usr/bin/env bash
set -euo pipefail

echo "[+] Installing Python tools..."
python3 -m pip install --user checkov

echo "[+] Checking required CLIs..."
for tool in terraform trivy checkov; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "[-] Missing: $tool"
  else
    echo "[+] Found: $tool"
  fi
done
