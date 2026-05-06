# CloudSec LabOps — Project Overview

CloudSec LabOps is a portfolio-grade cloud security engineering project.

It is designed to show practical skill across:

- Cloud misconfiguration detection and remediation
- IAM least privilege
- CI/CD security
- Kubernetes hardening
- Runtime detection
- CloudTrail detection engineering
- Container image scanning
- Policy-as-Code with OPA and Kyverno
- Secrets detection
- Attack path analysis
- Executive reporting

## Best Demo Path

Run:

```bash
bash scripts/run-local-demo.sh
```

or:

```bash
make quick
```

Then open:

```txt
docs/index.html
dashboard/lab10-executive-security-dashboard/output/executive-dashboard.html
```

## GitHub Pages

This repository includes `.github/workflows/pages.yml`.

After pushing to GitHub:

1. Go to repository Settings.
2. Open Pages.
3. Source: GitHub Actions.
4. Run the `Publish Portfolio Site` workflow.

## CV Line

**CloudSec LabOps — Cloud Security Engineering Portfolio**  
Built a hands-on cloud security lab covering Terraform, AWS IAM, GitHub Actions, Kubernetes, detection engineering, Trivy, OPA/Kyverno, secrets scanning, CloudTrail analysis, attack path modeling, and executive risk reporting.

## Interview Talking Points

- I built vulnerable and secure versions of cloud infrastructure.
- I wrote guardrails to prevent insecure changes in CI/CD.
- I created detection rules and sample logs to simulate incident response.
- I modeled chained attack paths instead of isolated findings.
- I generated an executive dashboard to communicate technical risk.
