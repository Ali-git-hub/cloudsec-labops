#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-terraform}"

echo "[+] Searching for dangerous IAM permissions in: $TARGET_DIR"

dangerous_patterns=(
  '"Action"[[:space:]]*:[[:space:]]*"\*"'
  '"Resource"[[:space:]]*:[[:space:]]*"\*"'
  'AdministratorAccess'
  'iam:PassRole'
  'iam:CreatePolicyVersion'
  'iam:AttachUserPolicy'
  'iam:AttachRolePolicy'
  'sts:AssumeRole'
)

found=0

for pattern in "${dangerous_patterns[@]}"; do
  if grep -RInE "$pattern" "$TARGET_DIR" --include="*.tf" --include="*.json"; then
    found=1
  fi
done

if [ "$found" -eq 1 ]; then
  echo "[-] Dangerous IAM pattern detected."
  exit 1
fi

echo "[+] No dangerous IAM patterns detected."
