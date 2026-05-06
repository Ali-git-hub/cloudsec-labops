# Lab 09 Report — Cloud Attack Path / Risk Graph

## Summary

This lab demonstrates graph-based cloud risk analysis.

Instead of evaluating misconfigurations independently, the graph connects exposures into realistic attack paths.

## Example Attack Path

Internet exposure can lead to a public S3 bucket. If that bucket contains a leaked GitHub token, an attacker may trigger CI/CD workflows, reach cloud credentials, escalate IAM privileges, disable CloudTrail, and compromise production.

## Why This Matters

Large companies care about security engineers who can connect small weaknesses into real business risk.

A single medium-severity issue may become critical when chained with:

- Public exposure.
- Secret leakage.
- CI/CD trust.
- IAM wildcard access.
- Logging disablement.
- Kubernetes privileged workload deployment.

## Run Analysis

```bash
python3 scripts/build-attack-graph.py attack-graph/lab09-cloud-risk-graph/data/cloud-assets.json
```

## Outputs

- JSON attack paths.
- Graphviz DOT graph.
- Markdown attack path report.

## Remediation Themes

- Remove public S3 exposure.
- Prevent secret leakage.
- Harden GitHub Actions.
- Use OIDC instead of static cloud keys.
- Enforce least privilege IAM.
- Alert on CloudTrail logging changes.
- Block privileged Kubernetes workloads.

## Skills Demonstrated

- Cloud attack path modeling
- Risk scoring
- Graph-based security analysis
- Detection engineering context
- Security reporting
