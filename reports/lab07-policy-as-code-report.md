# Lab 07 Report — Policy-as-Code with OPA and Kyverno

## Summary

This lab implements Kubernetes security guardrails using Policy-as-Code.

The goal is to prevent unsafe workloads before deployment.

## Controls Implemented

Kyverno policies enforce:

- No privileged containers.
- No hostPath volumes.
- Non-root container execution.

OPA/Rego policy detects:

- Privileged containers.
- hostPath volume usage.
- Missing `runAsNonRoot`.
- `allowPrivilegeEscalation: true`.

## Why This Matters

Without admission or CI policy checks, insecure manifests can reach production and create privilege escalation or host compromise risk.

## Test Results

The bad pod violates multiple controls:

- `privileged: true`
- `runAsUser: 0`
- `allowPrivilegeEscalation: true`
- `hostPath`

The good pod uses safer controls:

- `runAsNonRoot: true`
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- `capabilities.drop: ALL`
- `seccompProfile: RuntimeDefault`

## Run Validation

```bash
bash scripts/policy-as-code-guardrail.sh
```

Optional:

```bash
kyverno apply policy-as-code/lab07-opa-kyverno/kyverno-policies \
  --resource policy-as-code/lab07-opa-kyverno/test-manifests/violating
```

## Skills Demonstrated

- Kubernetes admission policy design
- Kyverno ClusterPolicy authoring
- OPA/Rego policy writing
- Shift-left security validation
- CI/CD policy enforcement
