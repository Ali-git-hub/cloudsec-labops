#!/usr/bin/env bash
set -euo pipefail

echo "======================================================"
echo " CloudSec LabOps — Local Demo Runner"
echo "======================================================"

run_allow_fail() {
  echo
  echo "[+] $1"
  shift
  set +e
  "$@"
  status=$?
  set -e
  if [ "$status" -ne 0 ]; then
    echo "[!] Security findings detected. Continuing because this is expected in demo mode."
  fi
}

run_allow_fail "Lab 08: Secrets Detection"   py scripts/secrets-detect.py secrets/lab08-secrets-detection/vulnerable

echo
echo "[+] Lab 08: Secure secrets validation"
py scripts/secrets-detect.py secrets/lab08-secrets-detection/secure

run_allow_fail "Lab 05: CloudTrail Detection"   py scripts/cloudtrail-detect.py     detections/lab05-cloudtrail-threat-detection/events/sample-cloudtrail.json     detections/lab05-cloudtrail-threat-detection/rules/cloudtrail-detections.yaml

run_allow_fail "Lab 09: Attack Graph"   py scripts/build-attack-graph.py attack-graph/lab09-cloud-risk-graph/data/cloud-assets.json

echo
echo "[+] Lab 10: Executive Dashboard"
py scripts/generate-executive-dashboard.py   dashboard/lab10-executive-security-dashboard/data/risk-register.json

echo
echo "[+] Building portfolio site"
py scripts/build-portfolio-site.py

echo
echo "======================================================"
echo " Demo complete"
echo " Open: docs/index.html"
echo " Open: dashboard/lab10-executive-security-dashboard/output/executive-dashboard.html"
echo "======================================================"
