# Lab 04 Report — Kubernetes Runtime Detection with Falco

## Summary

This lab demonstrates how risky Kubernetes workloads can be detected at runtime.

The vulnerable pod is intentionally misconfigured:

- Runs as root.
- Runs in privileged mode.
- Allows privilege escalation.
- Mounts the host filesystem using `hostPath`.

The secure pod applies common hardening controls:

- Runs as non-root.
- Drops Linux capabilities.
- Disables privilege escalation.
- Uses `RuntimeDefault` seccomp.
- Uses a read-only root filesystem.
- Avoids hostPath mounts.

## Attack Simulation

Deploy the vulnerable pod:

```bash
bash scripts/k8s-lab04-deploy-vulnerable.sh
```

Trigger suspicious behavior:

```bash
kubectl exec -it -n cloudsec-labops-vulnerable vulnerable-shell-pod -- sh
kubectl exec -n cloudsec-labops-vulnerable vulnerable-shell-pod -- cat /host/etc/hostname
```

## Detection Logic

Falco custom rules are stored in:

```txt
kubernetes/lab04-runtime-detection/falco/cloudsec-labops-rules.yaml
```

The rules detect:

- Shell spawned inside a container.
- Host filesystem access from a container.
- Package manager execution inside a running container.

## Remediation

Use the secure manifest in:

```txt
kubernetes/lab04-runtime-detection/secure/pod.yaml
```

## CI/CD Prevention

The repository includes:

```bash
bash scripts/k8s-manifest-security-scan.sh kubernetes
```

This fails builds when dangerous manifest patterns are detected.

## Skills Demonstrated

- Kubernetes workload hardening
- Runtime threat detection
- Falco custom rule writing
- Container security controls
- Security automation in CI/CD
