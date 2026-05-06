#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime

def get_nested(data, dotted_key):
    current = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current

def load_rules(path):
    # Minimal YAML-ish parser for this lab to avoid external dependencies.
    # Expected structure is simple and controlled.
    rules = []
    current = None

    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#") or stripped == "rules:":
            continue

        if stripped.startswith("- id:"):
            if current:
                rules.append(current)
            current = {"id": stripped.split(":", 1)[1].strip()}
            continue

        if current is None:
            continue

        if stripped.startswith("contains:"):
            current["contains"] = {}
            continue

        if stripped.startswith("field:"):
            current.setdefault("contains", {})["field"] = stripped.split(":", 1)[1].strip()
            continue

        if stripped.startswith("value:"):
            current.setdefault("contains", {})["value"] = stripped.split(":", 1)[1].strip()
            continue

        if ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()

    if current:
        rules.append(current)

    return rules

def event_matches_rule(event, rule):
    if event.get("eventSource") != rule.get("eventSource"):
        return False

    if event.get("eventName") != rule.get("eventName"):
        return False

    contains = rule.get("contains")
    if contains:
        value = get_nested(event, contains["field"])
        if value is None:
            return False
        return contains["value"] in str(value)

    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 scripts/cloudtrail-detect.py <events.json> <rules.yaml>")
        sys.exit(2)

    events_path = Path(sys.argv[1])
    rules_path = Path(sys.argv[2])

    data = json.loads(events_path.read_text(encoding="utf-8"))
    rules = load_rules(rules_path)

    findings = []
    for event in data.get("Records", []):
        for rule in rules:
            if event_matches_rule(event, rule):
                findings.append({
                    "rule_id": rule["id"],
                    "title": rule.get("title"),
                    "severity": rule.get("severity"),
                    "description": rule.get("description"),
                    "eventTime": event.get("eventTime"),
                    "eventSource": event.get("eventSource"),
                    "eventName": event.get("eventName"),
                    "principal": event.get("userIdentity", {}).get("arn"),
                    "sourceIPAddress": event.get("sourceIPAddress"),
                    "userAgent": event.get("userAgent"),
                    "requestParameters": event.get("requestParameters", {})
                })

    output_dir = Path("detections/lab05-cloudtrail-threat-detection/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "findings.json"
    output_path.write_text(json.dumps(findings, indent=2), encoding="utf-8")

    print(f"[+] Rules loaded: {len(rules)}")
    print(f"[+] Events analyzed: {len(data.get('Records', []))}")
    print(f"[+] Findings: {len(findings)}")
    print(f"[+] Output: {output_path}")

    for finding in findings:
        print(f"- [{finding['severity']}] {finding['title']} | {finding['principal']} | {finding['sourceIPAddress']}")

    if any(f.get("severity") == "critical" for f in findings):
        sys.exit(1)

if __name__ == "__main__":
    main()
