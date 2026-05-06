# Lab 10 Report — Executive Security Dashboard

## Summary

This lab converts technical cloud security work into executive-level reporting.

It aggregates all previous labs into a risk register and generates:

- HTML dashboard.
- JSON executive summary.
- Markdown report.

## Why This Matters

Strong cloud security engineers must communicate technical risk clearly to leadership.

This lab shows:

- What was vulnerable.
- What was detected.
- What was prevented.
- What was remediated.
- What evidence supports the claims.

## Metrics Included

- Total labs.
- Average risk score.
- Overall risk level.
- Critical finding count.
- Top risks.
- Risk register by domain.

## Run

```bash
python3 scripts/generate-executive-dashboard.py \
  dashboard/lab10-executive-security-dashboard/data/risk-register.json
```

## Skills Demonstrated

- Executive security reporting
- Risk register design
- Security metrics engineering
- Evidence mapping
- Portfolio presentation
