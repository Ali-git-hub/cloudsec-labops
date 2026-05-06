#!/usr/bin/env python3
import re
import sys
import json
from pathlib import Path

PATTERNS = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub Token", re.compile(r"ghp_[0-9A-Za-z]{36}")),
    ("Slack Webhook", re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9_/]+")),
    ("Postgres URL With Password", re.compile(r"postgres://[^:\s]+:[^@\s]+@[^/\s]+/[^\s]+")),
    ("Stripe Secret Key", re.compile(r"sk_live_[0-9A-Za-z]+")),
    ("AWS Secret Access Key Assignment", re.compile(r"AWS_SECRET_ACCESS_KEY\s*=\s*[^ \n]+")),
]

SKIP_DIRS = {".git", ".terraform", "node_modules", "__pycache__"}
TEXT_EXTS = {".py", ".env", ".txt", ".md", ".yaml", ".yml", ".json", ".toml", ".tf", ".sh"}

def should_scan(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    return path.is_file() and (path.suffix in TEXT_EXTS or path.name in {"Dockerfile", ".env"})

def mask(value: str) -> str:
    if len(value) <= 8:
        return "***"
    return value[:4] + "***" + value[-4:]

def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    findings = []

    for path in target.rglob("*"):
        if not should_scan(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for idx, line in enumerate(text.splitlines(), start=1):
            for name, pattern in PATTERNS:
                for match in pattern.finditer(line):
                    findings.append({
                        "type": name,
                        "file": str(path),
                        "line": idx,
                        "secret_preview": mask(match.group(0))
                    })

    output_dir = Path("secrets/lab08-secrets-detection/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "secrets-findings.json"
    output_path.write_text(json.dumps(findings, indent=2), encoding="utf-8")

    print(f"[+] Files scanned under: {target}")
    print(f"[+] Findings: {len(findings)}")
    print(f"[+] Output: {output_path}")

    for finding in findings:
        print(f"- {finding['type']} in {finding['file']}:{finding['line']} -> {finding['secret_preview']}")

    if findings:
        sys.exit(1)

if __name__ == "__main__":
    main()
