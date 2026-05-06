#!/usr/bin/env bash
set -euo pipefail

echo "[+] Deploying vulnerable Kubernetes lab..."
kubectl apply -f kubernetes/lab04-runtime-detection/vulnerable/namespace.yaml
kubectl apply -f kubernetes/lab04-runtime-detection/vulnerable/pod.yaml

echo "[+] Waiting for pod..."
kubectl wait --for=condition=Ready pod/vulnerable-shell-pod \
  -n cloudsec-labops-vulnerable \
  --timeout=120s

echo "[+] Vulnerable pod deployed."
echo "[+] Trigger detection:"
echo "kubectl exec -it -n cloudsec-labops-vulnerable vulnerable-shell-pod -- sh"
echo "kubectl exec -n cloudsec-labops-vulnerable vulnerable-shell-pod -- cat /host/etc/hostname"
