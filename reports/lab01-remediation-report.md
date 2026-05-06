# Lab 01 Remediation Report — Public S3 Exposure

## Summary

A Terraform configuration created an S3 bucket that allowed public object access. This is a common cloud security misconfiguration that can expose sensitive data to the internet.

## Impact

An attacker could access objects stored in the bucket without authentication if object keys are known or discoverable.

## Vulnerable Controls

The vulnerable configuration disabled all S3 public access block protections:

```hcl
block_public_acls       = false
block_public_policy     = false
ignore_public_acls      = false
restrict_public_buckets = false
```

It also created a public bucket policy:

```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:GetObject"
}
```

## Remediation

The secure configuration:

- Blocks public ACLs.
- Blocks public bucket policies.
- Ignores public ACLs.
- Restricts public buckets.
- Enables server-side encryption.
- Enables versioning.
- Enforces bucket-owner object ownership.

## Prevention

A GitHub Actions pipeline runs Checkov and Trivy on every push and pull request. Insecure infrastructure should fail CI before deployment.

## Skills Demonstrated

- Terraform security review
- AWS S3 hardening
- IaC scanning
- CI/CD security enforcement
- Security reporting
