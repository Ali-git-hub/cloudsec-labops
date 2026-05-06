#!/usr/bin/env bash
set -euo pipefail

echo "[+] Running Checkov IaC scan..."
checkov -d terraform --quiet

echo "[+] Running Trivy config scan..."
trivy config terraform

echo "[+] IaC scan completed."
