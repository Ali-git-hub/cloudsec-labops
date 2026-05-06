# Lab 03 Remediation Report — Insecure GitHub Actions Pipeline

## Summary

The vulnerable workflow demonstrates common CI/CD security risks in GitHub Actions:

- `pull_request_target` used on untrusted pull requests.
- `permissions: write-all`.
- Unpinned or unsafe action reference: `actions/checkout@master`.
- Secret exposure through logs.
- Remote script execution using `curl | bash`.

## Impact

A malicious contributor could potentially abuse the pipeline to access secrets, modify repository contents, or execute untrusted code with elevated permissions.

## Vulnerable Pattern

```yaml
on:
  pull_request_target:

permissions: write-all

steps:
  - uses: actions/checkout@master
  - run: echo "${{ secrets.AWS_SECRET_ACCESS_KEY }}"
  - run: curl https://example.com/install.sh | bash
```

## Secure Remediation

The secure workflow:

- Uses `push` to main instead of `pull_request_target` for deployment.
- Restricts permissions to only what is needed.
- Uses `actions/checkout@v4`.
- Uses AWS OIDC instead of long-lived static AWS keys.
- Avoids printing secrets.
- Avoids piping remote scripts directly into shell.

## CI/CD Prevention

The repository includes `scripts/detect-dangerous-github-actions.sh`, which blocks dangerous workflow patterns during CI.

## Skills Demonstrated

- CI/CD threat modeling
- GitHub Actions hardening
- Secret handling
- OIDC-based cloud authentication
- Pipeline security automation
