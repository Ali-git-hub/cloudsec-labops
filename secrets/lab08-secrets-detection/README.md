# Lab 08 — Secrets Detection and Prevention

This lab demonstrates how to detect hardcoded secrets and replace them with safe environment-variable based configuration.

## Vulnerable examples

```txt
secrets/lab08-secrets-detection/vulnerable/app.env
secrets/lab08-secrets-detection/vulnerable/config.py
```

## Secure examples

```txt
secrets/lab08-secrets-detection/secure/app.env.example
secrets/lab08-secrets-detection/secure/config.py
```

## Run custom detector

```bash
python3 scripts/secrets-detect.py secrets/lab08-secrets-detection/vulnerable
```

Expected result: findings are detected.

```bash
python3 scripts/secrets-detect.py secrets/lab08-secrets-detection/secure
```

Expected result: no findings.

## Run Gitleaks

```bash
gitleaks detect \
  --source secrets/lab08-secrets-detection/vulnerable \
  --config secrets/lab08-secrets-detection/gitleaks/gitleaks.toml \
  --no-git \
  --redact \
  --verbose
```
