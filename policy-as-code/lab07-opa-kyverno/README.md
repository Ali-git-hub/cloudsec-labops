# Lab 07 — Policy-as-Code with OPA and Kyverno

This lab demonstrates how to enforce Kubernetes security rules before workloads reach production.

## Policies

Kyverno policies:

- Disallow privileged containers.
- Require non-root execution.
- Disallow hostPath volumes.

OPA/Rego policy:

- Detect privileged containers.
- Detect hostPath volumes.
- Detect missing non-root controls.
- Detect privilege escalation.

## Test manifests

Violating manifest:

```txt
policy-as-code/lab07-opa-kyverno/test-manifests/violating/bad-pod.yaml
```

Passing manifest:

```txt
policy-as-code/lab07-opa-kyverno/test-manifests/passing/good-pod.yaml
```

## Run local guardrail

```bash
bash scripts/policy-as-code-guardrail.sh
```

## Optional Kyverno CLI test

```bash
kyverno apply policy-as-code/lab07-opa-kyverno/kyverno-policies \
  --resource policy-as-code/lab07-opa-kyverno/test-manifests/violating
```
