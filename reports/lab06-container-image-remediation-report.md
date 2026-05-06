# Lab 06 Remediation Report — Container Image Vulnerability Pipeline

## Summary

This lab demonstrates how insecure container images can introduce production risk, and how CI/CD can block weak Dockerfiles or vulnerable images.

## Vulnerable Image Risks

The vulnerable Dockerfile includes several bad practices:

```dockerfile
FROM python:3.9
ENV AWS_ACCESS_KEY_ID=AKIAEXAMPLELEAKEDKEY
ENV AWS_SECRET_ACCESS_KEY=do-not-hardcode-secrets
RUN apt-get update && apt-get install -y curl netcat-traditional vim
CMD ["python", "app.py"]
```

## Impact

These issues can lead to:

- Secret leakage through image layers.
- Larger attack surface.
- Root-level container compromise.
- Easier post-exploitation due to installed tools.
- Weak production reliability from development server usage.

## Secure Remediation

The secure Dockerfile:

- Uses a slim base image.
- Runs as a non-root user.
- Does not hardcode secrets.
- Uses Gunicorn.
- Avoids unnecessary OS tools.
- Uses `pip --no-cache-dir`.

## CI/CD Prevention

The pipeline includes:

```bash
bash scripts/container-dockerfile-guardrail.sh containers
```

and a Trivy image scan that fails on high or critical vulnerabilities.

## Skills Demonstrated

- Dockerfile security review
- Container hardening
- Secret hygiene
- Trivy image scanning
- CI/CD security enforcement
