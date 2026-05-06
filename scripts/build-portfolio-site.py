#!/usr/bin/env python3
from pathlib import Path
import json
import html
from datetime import datetime, timezone

ROOT = Path(".")
docs = ROOT / "docs"
docs.mkdir(exist_ok=True)

risk_path = ROOT / "dashboard/lab10-executive-security-dashboard/data/risk-register.json"
summary_path = ROOT / "dashboard/lab10-executive-security-dashboard/output/executive-summary.json"

risk = json.loads(risk_path.read_text(encoding="utf-8"))

if summary_path.exists():
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
else:
    avg = round(sum(x["risk_score"] for x in risk["labs"]) / len(risk["labs"]), 2)
    summary = {
        "total_labs": len(risk["labs"]),
        "average_risk_score": avg,
        "overall_risk_level": "Critical" if avg >= 9 else "High"
    }

cards = []
for lab in risk["labs"]:
    cards.append(f"""
      <article class="lab-card">
        <div class="lab-top">
          <span>{html.escape(lab['id'])}</span>
          <strong>{html.escape(lab['severity'].upper())}</strong>
        </div>
        <h3>{html.escape(lab['name'])}</h3>
        <p>{html.escape(lab['domain'])}</p>
        <p class="control">{html.escape(lab['control'])}</p>
        <div class="score">Risk Score: {lab['risk_score']}/10</div>
      </article>
    """)

html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>CloudSec LabOps</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{
      --bg: #020617;
      --panel: #0f172a;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --line: rgba(148, 163, 184, 0.22);
      --accent: #38bdf8;
      --accent2: #a78bfa;
      --danger: #fb7185;
      --good: #34d399;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 20% 10%, rgba(56,189,248,.18), transparent 30%),
        radial-gradient(circle at 80% 20%, rgba(167,139,250,.18), transparent 30%),
        var(--bg);
      color: var(--text);
    }}
    header {{
      min-height: 76vh;
      display: grid;
      place-items: center;
      padding: 48px 24px;
      border-bottom: 1px solid var(--line);
    }}
    .hero {{ max-width: 1120px; width: 100%; }}
    .badge {{
      display: inline-flex;
      border: 1px solid var(--line);
      color: var(--accent);
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(15,23,42,.72);
      font-weight: 700;
      font-size: 14px;
    }}
    h1 {{
      font-size: clamp(44px, 8vw, 92px);
      line-height: .95;
      letter-spacing: -0.07em;
      margin: 28px 0;
      max-width: 980px;
    }}
    .gradient {{
      background: linear-gradient(90deg, var(--accent), var(--accent2), var(--danger));
      -webkit-background-clip: text;
      color: transparent;
    }}
    .lead {{
      color: var(--muted);
      font-size: clamp(18px, 2.4vw, 24px);
      max-width: 820px;
      line-height: 1.55;
    }}
    .actions {{
      display: flex;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 30px;
    }}
    .btn {{
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 14px 18px;
      background: rgba(15,23,42,.8);
      text-decoration: none;
      color: white;
      font-weight: 800;
    }}
    .btn.primary {{ background: linear-gradient(90deg, #0284c7, #7c3aed); border: none; }}
    main {{ max-width: 1180px; margin: auto; padding: 48px 24px; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: -96px;
      margin-bottom: 56px;
      position: relative;
      z-index: 2;
    }}
    .metric, .lab-card, .section {{
      background: rgba(15,23,42,.82);
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 24px;
      box-shadow: 0 24px 70px rgba(0,0,0,.28);
    }}
    .metric span {{ display: block; color: var(--muted); margin-bottom: 10px; }}
    .metric strong {{ font-size: 34px; }}
    .section {{ margin: 28px 0; }}
    .section h2 {{ font-size: 34px; letter-spacing: -0.04em; margin-top: 0; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-top: 22px;
    }}
    .lab-card h3 {{ margin: 14px 0 8px; font-size: 20px; }}
    .lab-card p {{ color: var(--muted); line-height: 1.5; }}
    .lab-top {{
      display: flex;
      justify-content: space-between;
      color: var(--accent);
      font-weight: 900;
      font-size: 13px;
    }}
    .control {{ min-height: 52px; }}
    .score {{ margin-top: 16px; color: var(--good); font-weight: 900; }}
    pre {{
      white-space: pre-wrap;
      background: #020617;
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      overflow-x: auto;
      color: #c4b5fd;
    }}
    footer {{
      color: var(--muted);
      padding: 48px 24px;
      text-align: center;
      border-top: 1px solid var(--line);
    }}
    @media (max-width: 800px) {{
      .metrics {{ grid-template-columns: 1fr; margin-top: 0; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <div class="badge">Cloud Security Portfolio Project</div>
      <h1>CloudSec LabOps: <span class="gradient">attack, detect, remediate, prevent.</span></h1>
      <p class="lead">
        A hands-on cloud security engineering lab covering AWS, IAM, CI/CD, Kubernetes,
        runtime detection, secrets, containers, policy-as-code, attack graphs, and executive reporting.
      </p>
      <div class="actions">
        <a class="btn primary" href="../dashboard/lab10-executive-security-dashboard/output/executive-dashboard.html">Open Executive Dashboard</a>
        <a class="btn" href="../attack-graph/lab09-cloud-risk-graph/output/attack-path-report.md">Attack Path Report</a>
      </div>
    </div>
  </header>

  <main>
    <section class="metrics">
      <div class="metric"><span>Total Labs</span><strong>{summary.get('total_labs')}</strong></div>
      <div class="metric"><span>Average Risk</span><strong>{summary.get('average_risk_score')}/10</strong></div>
      <div class="metric"><span>Risk Level</span><strong>{summary.get('overall_risk_level')}</strong></div>
    </section>

    <section class="section">
      <h2>How to run the demo</h2>
      <p class="lead">Run the safest local demo path without AWS or Kubernetes credentials.</p>
      <pre>bash scripts/run-local-demo.sh

# or
make quick</pre>
    </section>

    <section class="section">
      <h2>Security Labs</h2>
      <div class="grid">
        {''.join(cards)}
      </div>
    </section>

    <section class="section">
      <h2>Hiring Signal</h2>
      <p class="lead">
        This project is designed to prove real security engineering ability:
        secure-by-default infrastructure, detection-as-code, CI/CD guardrails,
        cloud risk analysis, and leadership-ready reporting.
      </p>
    </section>
  </main>

  <footer>
    Generated {datetime.now(timezone.utc).isoformat()} · CloudSec LabOps
  </footer>
</body>
</html>
"""

(docs / "index.html").write_text(html_doc, encoding="utf-8")
print("[+] Generated docs/index.html")
