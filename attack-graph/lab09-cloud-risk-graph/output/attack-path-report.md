# Lab 09 Attack Path Report — Cloud Risk Graph

## Summary

This report identifies attack paths from internet exposure to crown-jewel cloud assets.

## Critical Attack Paths

### Path 1 — Score 21

Internet -> Public S3 Bucket -> Leaked GitHub Token -> GitHub Actions Pipeline -> Developer IAM User -> AdministratorAccess Policy -> Production AWS Account

| Step | Relationship | Risk |
|---|---|---|
| Internet → Public S3 Bucket | can_read_public_objects | high |
| Public S3 Bucket → Leaked GitHub Token | contains_secret | critical |
| Leaked GitHub Token → GitHub Actions Pipeline | can_trigger_pipeline | high |
| GitHub Actions Pipeline → Developer IAM User | uses_cloud_credentials | high |
| Developer IAM User → AdministratorAccess Policy | can_attach_policy | critical |
| AdministratorAccess Policy → Production AWS Account | grants_admin_access | critical |

## Recommended Controls

- Block public S3 access and scan buckets for exposed secrets.
- Replace long-lived cloud keys with OIDC-based federation.
- Remove wildcard IAM permissions and enforce least privilege.
- Alert on CloudTrail StopLogging and DeleteTrail.
- Enforce Kubernetes admission policies for privileged pods and hostPath.
- Add secret scanning and CI/CD workflow hardening.