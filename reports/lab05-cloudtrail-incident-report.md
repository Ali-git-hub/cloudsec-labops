# Lab 05 Incident Report — CloudTrail Threat Detection

## Summary

This lab analyzes CloudTrail-style events and detects suspicious AWS activity using custom detection rules.

The sample event set includes:

- IAM access key creation.
- AdministratorAccess policy attachment.
- CloudTrail logging disabled.
- Benign S3 ListBuckets activity.

## Detection Findings

The detection engine flags:

1. `CreateAccessKey`
2. `AttachUserPolicy` with `AdministratorAccess`
3. `StopLogging` for CloudTrail

The most severe finding is CloudTrail logging being stopped, which may indicate an attacker attempting to hide activity.

## Attack Timeline

| Time UTC | Event | Risk |
|---|---|---|
| 2026-05-05 09:10 | CreateAccessKey | Persistence |
| 2026-05-05 09:12 | AttachUserPolicy AdministratorAccess | Privilege escalation |
| 2026-05-05 09:13 | StopLogging | Defense evasion |

## Run Detection

```bash
python3 scripts/cloudtrail-detect.py \
  detections/lab05-cloudtrail-threat-detection/events/sample-cloudtrail.json \
  detections/lab05-cloudtrail-threat-detection/rules/cloudtrail-detections.yaml
```

## Expected Output

The script writes findings to:

```txt
detections/lab05-cloudtrail-threat-detection/output/findings.json
```

## Remediation

Immediate actions:

- Re-enable CloudTrail logging.
- Rotate and disable suspicious access keys.
- Remove unauthorized AdministratorAccess policy attachments.
- Review all IAM changes from the source IP.
- Check for persistence through new users, roles, policies, and access keys.
- Confirm CloudTrail logs are delivered to a protected S3 bucket.
- Enable alerts on CloudTrail `StopLogging`, `DeleteTrail`, and IAM privilege escalation events.

## Skills Demonstrated

- AWS detection engineering
- CloudTrail event analysis
- Detection-as-code
- Incident timeline reconstruction
- Security automation with CI
