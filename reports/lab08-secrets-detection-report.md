# Lab 08 Report — Secrets Detection and Prevention

## Summary

This lab demonstrates secret leakage detection and remediation.

The vulnerable examples intentionally include fake credentials:

- AWS access key pattern.
- AWS secret key assignment.
- GitHub token pattern.
- Slack webhook URL.
- Database URL with embedded password.
- Stripe live secret key pattern.

## Impact

Hardcoded secrets can lead to:

- Unauthorized cloud access.
- CI/CD compromise.
- Data exfiltration.
- Lateral movement.
- Persistence through stolen tokens.

## Detection

The lab includes two detection methods:

1. Custom Python detector:

```bash
python3 scripts/secrets-detect.py secrets/lab08-secrets-detection/vulnerable
```

2. Gitleaks configuration:

```txt
secrets/lab08-secrets-detection/gitleaks/gitleaks.toml
```

## Remediation

The secure implementation:

- Uses `.env.example` without real values.
- Reads secrets from environment variables.
- Fails fast when required environment variables are missing.
- Avoids storing credentials in source control.

## Prevention

CI runs detection against secure folders. A real production repository should scan the full repository and block merges when secrets are detected.

## Skills Demonstrated

- Secrets detection engineering
- Regex-based detection
- Gitleaks configuration
- Secure configuration design
- CI/CD secret prevention
