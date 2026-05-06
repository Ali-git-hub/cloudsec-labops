#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-cloudsec-labops-secure:latest}"
CONTEXT_DIR="containers/lab06-image-vulnerability-pipeline"
DOCKERFILE="$CONTEXT_DIR/secure/Dockerfile"

echo "[+] Building secure container image: $IMAGE_NAME"
docker build -f "$DOCKERFILE" -t "$IMAGE_NAME" "$CONTEXT_DIR"

echo "[+] Scanning image with Trivy..."
trivy image --exit-code 1 --severity HIGH,CRITICAL "$IMAGE_NAME"

echo "[+] Container image scan passed."
