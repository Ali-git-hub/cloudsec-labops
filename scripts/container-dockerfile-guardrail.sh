#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-containers}"

echo "[+] Checking Dockerfiles for dangerous patterns in: $TARGET_DIR"

dangerous_patterns=(
  '^FROM .*:latest'
  '^USER root'
  'AWS_ACCESS_KEY_ID='
  'AWS_SECRET_ACCESS_KEY='
  'apt-get install -y .*vim'
  'apt-get install -y .*netcat'
  'curl .*\\|[[:space:]]*bash'
  'CMD \\["python", "app.py"\\]'
)

found=0

for pattern in "${dangerous_patterns[@]}"; do
  if grep -RInE "$pattern" "$TARGET_DIR" --include="Dockerfile"; then
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  echo "[-] Dangerous Dockerfile pattern detected."
  exit 1
fi

echo "[+] Dockerfile guardrail scan passed."
