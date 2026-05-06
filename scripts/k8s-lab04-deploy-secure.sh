#!/usr/bin/env bash
set -euo pipefail

echo "[+] Deploying secure Kubernetes lab..."
kubectl apply -f kubernetes/lab04-runtime-detection/secure/namespace.yaml
kubectl apply -f kubernetes/lab04-runtime-detection/secure/pod.yaml

echo "[+] Waiting for pod..."
kubectl wait --for=condition=Ready pod/secure-app-pod \
  -n cloudsec-labops-secure \
  --timeout=120s

echo "[+] Secure pod deployed."
