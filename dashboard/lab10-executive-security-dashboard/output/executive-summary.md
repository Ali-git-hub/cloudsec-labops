# CloudSec LabOps — Executive Security Summary

Generated: 2026-05-06T15:25:33.422900+00:00

## Metrics

- Total labs: 9
- Average risk score: 8.78/10
- Overall risk level: High
- Critical findings: 5

## Top Risks

- **LAB-02 — IAM Privilege Escalation Risk**: 10/10, critical
- **LAB-05 — CloudTrail Threat Detection**: 10/10, critical
- **LAB-09 — Attack Path / Cloud Risk Graph**: 10/10, critical
- **LAB-04 — Kubernetes Runtime Detection**: 9/10, critical
- **LAB-08 — Secrets Detection and Prevention**: 9/10, critical

## Risk Register

| Lab | Domain | Severity | Status | Risk | Control |
|---|---|---|---|---:|---|
| LAB-02 IAM Privilege Escalation Risk | Identity and Access | critical | remediated | 10 | Least privilege IAM policy |
| LAB-05 CloudTrail Threat Detection | Detection Engineering | critical | detected | 10 | Detection rules for IAM and CloudTrail events |
| LAB-09 Attack Path / Cloud Risk Graph | Risk Management | critical | analyzed | 10 | Attack path modeling and remediation mapping |
| LAB-04 Kubernetes Runtime Detection | Runtime Security | critical | detected | 9 | Falco detection and hardened pod spec |
| LAB-08 Secrets Detection and Prevention | Secrets Security | critical | prevented | 9 | Custom detector and Gitleaks |
| LAB-01 Public S3 Exposure | Cloud Infrastructure | high | remediated | 8 | Block public access, encryption, versioning |
| LAB-03 Insecure GitHub Actions Pipeline | CI/CD Security | high | remediated | 8 | Pinned actions, least permissions, OIDC |
| LAB-07 Policy-as-Code with OPA and Kyverno | Kubernetes Governance | high | prevented | 8 | Kyverno and OPA guardrails |
| LAB-06 Container Image Vulnerability Pipeline | Container Security | high | remediated | 7 | Trivy scan and hardened Dockerfile |

## Portfolio Value

This project demonstrates practical cloud security engineering across prevention, detection, response, and executive communication.