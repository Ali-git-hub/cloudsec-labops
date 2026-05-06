# Lab 10 — Executive Security Dashboard

This lab generates an executive dashboard from the CloudSec LabOps risk register.

## Input

```txt
dashboard/lab10-executive-security-dashboard/data/risk-register.json
```

## Generate dashboard

```bash
python3 scripts/generate-executive-dashboard.py \
  dashboard/lab10-executive-security-dashboard/data/risk-register.json
```

## Outputs

```txt
dashboard/lab10-executive-security-dashboard/output/executive-dashboard.html
dashboard/lab10-executive-security-dashboard/output/executive-summary.json
dashboard/lab10-executive-security-dashboard/output/executive-summary.md
```

Open the HTML file in a browser to view the dashboard.

## What this proves

- Executive-level security communication
- Risk scoring
- Security metrics
- Evidence-based reporting
- Cloud security portfolio presentation
