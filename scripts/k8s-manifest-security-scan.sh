#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-kubernetes}"

echo "[+] Running Kubernetes manifest security checks against: $TARGET_DIR"

dangerous_patterns=(
  'privileged:[[:space:]]*true'
  'allowPrivilegeEscalation:[[:space:]]*true'
  'runAsUser:[[:space:]]*0'
  'hostPath:'
  'hostNetwork:[[:space:]]*true'
  'hostPID:[[:space:]]*true'
  'hostIPC:[[:space:]]*true'
)

found=0

for pattern in "${dangerous_patterns[@]}"; do
  if grep -RInE "$pattern" "$TARGET_DIR" --include="*.yaml" --include="*.yml"; then
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  echo "[-] Dangerous Kubernetes manifest pattern detected."
  exit 1
fi

echo "[+] No dangerous Kubernetes manifest patterns detected."
