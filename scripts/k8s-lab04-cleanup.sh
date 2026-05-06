#!/usr/bin/env bash
set -euo pipefail

echo "[+] Cleaning Lab 04 namespaces..."
kubectl delete namespace cloudsec-labops-vulnerable --ignore-not-found=true
kubectl delete namespace cloudsec-labops-secure --ignore-not-found=true
echo "[+] Cleanup complete."
