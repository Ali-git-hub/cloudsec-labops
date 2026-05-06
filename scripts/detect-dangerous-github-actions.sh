#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-.github/workflows cicd-security}"

echo "[+] Searching for dangerous GitHub Actions patterns..."

dangerous_patterns=(
  'pull_request_target'
  'permissions:[[:space:]]*write-all'
  'actions/checkout@master'
  'curl .*\\|[[:space:]]*bash'
  'wget .*\\|[[:space:]]*bash'
  'secrets\.[A-Z0-9_]+'
  'echo .*secrets\.'
)

found=0

for target in $TARGET_DIR; do
  [ -e "$target" ] || continue

  for pattern in "${dangerous_patterns[@]}"; do
    if grep -RInE "$pattern" "$target" --include="*.yml" --include="*.yaml"; then
      found=1
    fi
  done
done

if [ "$found" -eq 1 ]; then
  echo "[-] Dangerous GitHub Actions pattern detected."
  exit 1
fi

echo "[+] No dangerous GitHub Actions patterns detected."
