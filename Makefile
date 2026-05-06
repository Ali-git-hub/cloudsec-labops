SHELL := /bin/bash

.PHONY: help quick secrets cloudtrail attack-graph dashboard validate clean

help:
	@echo "CloudSec LabOps commands:"
	@echo "  make quick             Run the safest local labs and generate reports"
	@echo "  make secrets           Run secrets detection lab"
	@echo "  make cloudtrail        Run CloudTrail detection lab"
	@echo "  make attack-graph      Generate cloud risk graph outputs"
	@echo "  make dashboard         Generate executive dashboard and portfolio site"
	@echo "  make validate          Run lightweight guardrails"
	@echo "  make clean             Remove generated outputs"

quick: secrets cloudtrail attack-graph dashboard
	@echo "[+] Quick demo complete. Open docs/index.html or dashboard output."

secrets:
	@echo "[+] Running Lab 08 secrets detection against vulnerable examples..."
	@set +e; python3 scripts/secrets-detect.py secrets/lab08-secrets-detection/vulnerable; true
	@echo "[+] Validating secure secrets examples..."
	@python3 scripts/secrets-detect.py secrets/lab08-secrets-detection/secure

cloudtrail:
	@echo "[+] Running Lab 05 CloudTrail detection..."
	@set +e; python3 scripts/cloudtrail-detect.py detections/lab05-cloudtrail-threat-detection/events/sample-cloudtrail.json detections/lab05-cloudtrail-threat-detection/rules/cloudtrail-detections.yaml; true

attack-graph:
	@echo "[+] Running Lab 09 attack graph..."
	@set +e; python3 scripts/build-attack-graph.py attack-graph/lab09-cloud-risk-graph/data/cloud-assets.json; true

dashboard:
	@echo "[+] Generating Lab 10 executive dashboard..."
	@python3 scripts/generate-executive-dashboard.py dashboard/lab10-executive-security-dashboard/data/risk-register.json
	@python3 scripts/build-portfolio-site.py

validate:
	@echo "[+] Running lightweight validations..."
	@bash scripts/policy-as-code-guardrail.sh
	@bash scripts/container-dockerfile-guardrail.sh containers/ || true
	@bash scripts/k8s-manifest-security-scan.sh kubernetes/ || true
	@bash scripts/detect-dangerous-github-actions.sh ".github/workflows cicd-security" || true
	@bash scripts/detect-dangerous-iam.sh terraform || true

clean:
	@rm -rf detections/lab05-cloudtrail-threat-detection/output
	@rm -rf secrets/lab08-secrets-detection/output
	@rm -rf attack-graph/lab09-cloud-risk-graph/output
	@rm -rf dashboard/lab10-executive-security-dashboard/output
	@echo "[+] Generated outputs removed."
