#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict
import html

SEVERITY_WEIGHT = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

STATUS_COLOR = {
    "remediated": "#dcfce7",
    "detected": "#dbeafe",
    "prevented": "#fef9c3",
    "analyzed": "#ede9fe"
}

def risk_level(score):
    if score >= 9:
        return "Critical"
    if score >= 7:
        return "High"
    if score >= 4:
        return "Medium"
    return "Low"

def generate_summary(data):
    labs = data["labs"]
    total = len(labs)
    avg_score = round(sum(item["risk_score"] for item in labs) / total, 2)
    severity_counts = Counter(item["severity"] for item in labs)
    status_counts = Counter(item["status"] for item in labs)
    domain_counts = Counter(item["domain"] for item in labs)

    top_risks = sorted(labs, key=lambda item: item["risk_score"], reverse=True)[:5]

    return {
        "project": data["project"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_labs": total,
        "average_risk_score": avg_score,
        "overall_risk_level": risk_level(avg_score),
        "severity_counts": dict(severity_counts),
        "status_counts": dict(status_counts),
        "domain_counts": dict(domain_counts),
        "top_risks": top_risks
    }

def table_rows(labs):
    rows = []
    for item in sorted(labs, key=lambda row: row["risk_score"], reverse=True):
        status_bg = STATUS_COLOR.get(item["status"], "#f8fafc")
        rows.append(f"""
        <tr>
          <td>{html.escape(item['id'])}</td>
          <td>{html.escape(item['name'])}</td>
          <td>{html.escape(item['domain'])}</td>
          <td><span class="sev {html.escape(item['severity'])}">{html.escape(item['severity'].upper())}</span></td>
          <td>{item['risk_score']}/10</td>
          <td><span class="status" style="background:{status_bg}">{html.escape(item['status'])}</span></td>
          <td>{html.escape(item['control'])}</td>
          <td><code>{html.escape(item['evidence'])}</code></td>
        </tr>
        """)
    return "\n".join(rows)

def count_cards(summary):
    sev = summary["severity_counts"]
    status = summary["status_counts"]
    return f"""
      <div class="card"><div class="label">Total Labs</div><div class="value">{summary['total_labs']}</div></div>
      <div class="card"><div class="label">Average Risk</div><div class="value">{summary['average_risk_score']}/10</div></div>
      <div class="card"><div class="label">Overall Level</div><div class="value">{summary['overall_risk_level']}</div></div>
      <div class="card"><div class="label">Critical Findings</div><div class="value">{sev.get('critical', 0)}</div></div>
      <div class="card"><div class="label">Prevented</div><div class="value">{status.get('prevented', 0)}</div></div>
      <div class="card"><div class="label">Remediated</div><div class="value">{status.get('remediated', 0)}</div></div>
    """

def generate_html(data, summary):
    rows = table_rows(data["labs"])
    cards = count_cards(summary)

    top_risk_items = "\n".join(
        f"<li><strong>{html.escape(item['id'])}</strong> — {html.escape(item['name'])} ({item['risk_score']}/10)</li>"
        for item in summary["top_risks"]
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>CloudSec LabOps Executive Security Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      margin: 0;
      background: #f8fafc;
      color: #0f172a;
    }}
    header {{
      background: #0f172a;
      color: white;
      padding: 32px;
    }}
    main {{
      padding: 32px;
      max-width: 1400px;
      margin: 0 auto;
    }}
    h1, h2 {{
      margin: 0 0 12px;
    }}
    .subtitle {{
      color: #cbd5e1;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin: 24px 0;
    }}
    .card {{
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 20px;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }}
    .label {{
      color: #64748b;
      font-size: 14px;
    }}
    .value {{
      font-size: 32px;
      font-weight: 800;
      margin-top: 8px;
    }}
    section {{
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 16px;
      padding: 24px;
      margin: 24px 0;
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      padding: 12px;
      border-bottom: 1px solid #e2e8f0;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #f1f5f9;
      color: #334155;
    }}
    code {{
      background: #f1f5f9;
      padding: 2px 6px;
      border-radius: 6px;
    }}
    .sev, .status {{
      display: inline-block;
      border-radius: 999px;
      padding: 4px 10px;
      font-weight: 700;
      font-size: 12px;
    }}
    .critical {{ background: #fee2e2; color: #991b1b; }}
    .high {{ background: #ffedd5; color: #9a3412; }}
    .medium {{ background: #fef9c3; color: #854d0e; }}
    .low {{ background: #dcfce7; color: #166534; }}
    .footer {{
      color: #64748b;
      font-size: 13px;
      margin-top: 24px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>CloudSec LabOps — Executive Security Dashboard</h1>
    <p class="subtitle">Portfolio-grade cloud security program summary generated from hands-on labs.</p>
  </header>
  <main>
    <div class="grid">
      {cards}
    </div>

    <section>
      <h2>Executive Summary</h2>
      <p>
        This dashboard summarizes cloud security risks across infrastructure, IAM, CI/CD,
        Kubernetes, container images, detection engineering, secrets, and attack path analysis.
      </p>
      <p>
        The project demonstrates prevention, detection, remediation, and reporting across a realistic
        cloud security lifecycle.
      </p>
    </section>

    <section>
      <h2>Top Risks</h2>
      <ol>
        {top_risk_items}
      </ol>
    </section>

    <section>
      <h2>Risk Register</h2>
      <table>
        <thead>
          <tr>
            <th>Lab</th>
            <th>Name</th>
            <th>Domain</th>
            <th>Severity</th>
            <th>Risk</th>
            <th>Status</th>
            <th>Control</th>
            <th>Evidence</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </section>

    <section>
      <h2>What This Proves</h2>
      <ul>
        <li>Cloud misconfiguration detection and remediation.</li>
        <li>IAM least-privilege engineering.</li>
        <li>CI/CD and secrets security automation.</li>
        <li>Kubernetes hardening and runtime detection.</li>
        <li>Policy-as-Code enforcement.</li>
        <li>Attack path analysis and executive reporting.</li>
      </ul>
    </section>

    <div class="footer">
      Generated at {html.escape(summary['generated_at'])}
    </div>
  </main>
</body>
</html>
"""

def generate_markdown(data, summary):
    lines = [
        "# CloudSec LabOps — Executive Security Summary",
        "",
        f"Generated: {summary['generated_at']}",
        "",
        "## Metrics",
        "",
        f"- Total labs: {summary['total_labs']}",
        f"- Average risk score: {summary['average_risk_score']}/10",
        f"- Overall risk level: {summary['overall_risk_level']}",
        f"- Critical findings: {summary['severity_counts'].get('critical', 0)}",
        "",
        "## Top Risks",
        ""
    ]

    for item in summary["top_risks"]:
        lines.append(f"- **{item['id']} — {item['name']}**: {item['risk_score']}/10, {item['severity']}")

    lines.extend([
        "",
        "## Risk Register",
        "",
        "| Lab | Domain | Severity | Status | Risk | Control |",
        "|---|---|---|---|---:|---|"
    ])

    for item in sorted(data["labs"], key=lambda row: row["risk_score"], reverse=True):
        lines.append(
            f"| {item['id']} {item['name']} | {item['domain']} | {item['severity']} | {item['status']} | {item['risk_score']} | {item['control']} |"
        )

    lines.extend([
        "",
        "## Portfolio Value",
        "",
        "This project demonstrates practical cloud security engineering across prevention, detection, response, and executive communication."
    ])

    return "\n".join(lines)

def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dashboard/lab10-executive-security-dashboard/data/risk-register.json")
    output_dir = Path("dashboard/lab10-executive-security-dashboard/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    summary = generate_summary(data)

    (output_dir / "executive-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (output_dir / "executive-dashboard.html").write_text(generate_html(data, summary), encoding="utf-8")
    (output_dir / "executive-summary.md").write_text(generate_markdown(data, summary), encoding="utf-8")

    print(f"[+] Dashboard generated: {output_dir / 'executive-dashboard.html'}")
    print(f"[+] Summary generated: {output_dir / 'executive-summary.json'}")
    print(f"[+] Markdown report generated: {output_dir / 'executive-summary.md'}")

if __name__ == "__main__":
    main()
