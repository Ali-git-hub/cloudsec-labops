#!/usr/bin/env bash
set -euo pipefail

VIOLATING_DIR="policy-as-code/lab07-opa-kyverno/test-manifests/violating"
PASSING_DIR="policy-as-code/lab07-opa-kyverno/test-manifests/passing"

echo "[+] Running lightweight Policy-as-Code guardrail checks..."

dangerous_patterns=(
  'privileged:[[:space:]]*true'
  'allowPrivilegeEscalation:[[:space:]]*true'
  'runAsUser:[[:space:]]*0'
  'hostPath:'
)

found=0

echo "[+] Checking violating manifests should trigger findings..."
for pattern in "${dangerous_patterns[@]}"; do
  if grep -RInE "$pattern" "$VIOLATING_DIR" --include="*.yaml" --include="*.yml"; then
    found=1
  fi
done

if [ "$found" -eq 0 ]; then
  echo "[-] Expected violating manifests to contain risky patterns, but none were found."
  exit 1
fi

echo "[+] Checking passing manifests should not contain risky patterns..."
for pattern in "${dangerous_patterns[@]}"; do
  if grep -RInE "$pattern" "$PASSING_DIR" --include="*.yaml" --include="*.yml"; then
    echo "[-] Passing manifest contains risky pattern: $pattern"
    exit 1
  fi
done

echo "[+] Policy-as-Code guardrail check passed."
