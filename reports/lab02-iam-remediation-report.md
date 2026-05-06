# Lab 02 Remediation Report — IAM Privilege Escalation Risk

## Summary

The vulnerable Terraform configuration creates an IAM user with full administrative access:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

This is a critical cloud security issue because any leaked access key or compromised user could control the AWS account.

## Impact

An attacker with this user's credentials could:

- Create new IAM users.
- Attach admin policies.
- Disable logging.
- Access or delete data.
- Create persistence.
- Escalate privileges further through IAM and STS actions.

## Root Cause

The IAM policy grants unrestricted actions on unrestricted resources. This violates least-privilege access design.

## Secure Remediation

The secure version replaces admin access with scoped read-only S3 access:

- `s3:ListBucket` only on one specific bucket.
- `s3:GetObject` only for objects inside that bucket.
- No IAM permissions.
- No wildcard admin access.
- No access key is generated in the secure version.

## CI/CD Prevention

The repository includes `scripts/detect-dangerous-iam.sh`, which fails when it detects common dangerous IAM patterns such as:

- `Action = "*"`
- `Resource = "*"`
- `AdministratorAccess`
- `iam:PassRole`
- `iam:CreatePolicyVersion`
- `sts:AssumeRole`

## Skills Demonstrated

- IAM security review
- Least-privilege policy design
- Terraform security engineering
- CI/CD guardrails
- Privilege escalation risk analysis
