#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from collections import defaultdict, deque

RISK_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

def load_graph(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in data["nodes"]}
    edges = data["edges"]
    adjacency = defaultdict(list)

    for edge in edges:
        adjacency[edge["from"]].append(edge)

    return data, nodes, edges, adjacency

def find_paths(adjacency, start, targets, max_depth=8):
    paths = []
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()

        if len(path) > max_depth:
            continue

        if current in targets and path:
            paths.append(path)
            continue

        for edge in adjacency.get(current, []):
            next_node = edge["to"]

            if any(e["from"] == next_node for e in path):
                continue

            queue.append((next_node, path + [edge]))

    return paths

def score_path(path):
    return sum(RISK_SCORE.get(edge.get("risk", "low"), 1) for edge in path)

def path_to_nodes(path):
    if not path:
        return []
    nodes = [path[0]["from"]]
    nodes.extend(edge["to"] for edge in path)
    return nodes

def generate_dot(nodes, edges, critical_paths):
    critical_edges = {
        (edge["from"], edge["to"])
        for path in critical_paths
        for edge in path["edges"]
    }

    lines = [
        "digraph CloudRiskGraph {",
        '  rankdir="LR";',
        '  node [shape=box, style="rounded"];'
    ]

    for node_id, node in nodes.items():
        label = f'{node["label"]}\\n{node["type"]}'
        risk = node.get("risk", "low")
        if risk == "critical":
            style = 'style="rounded,filled", fillcolor="#ffcccc"'
        elif risk == "high":
            style = 'style="rounded,filled", fillcolor="#ffe0b3"'
        else:
            style = 'style="rounded"'
        lines.append(f'  "{node_id}" [label="{label}", {style}];')

    for edge in edges:
        attrs = []
        label = edge["relationship"]
        attrs.append(f'label="{label}"')
        if (edge["from"], edge["to"]) in critical_edges:
            attrs.append('color="red"')
            attrs.append('penwidth="2"')
        lines.append(f'  "{edge["from"]}" -> "{edge["to"]}" [{", ".join(attrs)}];')

    lines.append("}")
    return "\n".join(lines)

def generate_markdown(nodes, critical_paths):
    lines = [
        "# Lab 09 Attack Path Report — Cloud Risk Graph",
        "",
        "## Summary",
        "",
        "This report identifies attack paths from internet exposure to crown-jewel cloud assets.",
        "",
        "## Critical Attack Paths",
        ""
    ]

    if not critical_paths:
        lines.append("No critical paths detected.")
        return "\n".join(lines)

    for idx, item in enumerate(critical_paths, start=1):
        node_ids = path_to_nodes(item["edges"])
        labels = [nodes[node_id]["label"] for node_id in node_ids]
        lines.append(f"### Path {idx} — Score {item['score']}")
        lines.append("")
        lines.append(" -> ".join(labels))
        lines.append("")
        lines.append("| Step | Relationship | Risk |")
        lines.append("|---|---|---|")
        for edge in item["edges"]:
            lines.append(f"| {nodes[edge['from']]['label']} → {nodes[edge['to']]['label']} | {edge['relationship']} | {edge['risk']} |")
        lines.append("")

    lines.extend([
        "## Recommended Controls",
        "",
        "- Block public S3 access and scan buckets for exposed secrets.",
        "- Replace long-lived cloud keys with OIDC-based federation.",
        "- Remove wildcard IAM permissions and enforce least privilege.",
        "- Alert on CloudTrail StopLogging and DeleteTrail.",
        "- Enforce Kubernetes admission policies for privileged pods and hostPath.",
        "- Add secret scanning and CI/CD workflow hardening."
    ])

    return "\n".join(lines)

def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("attack-graph/lab09-cloud-risk-graph/data/cloud-assets.json")
    output_dir = Path("attack-graph/lab09-cloud-risk-graph/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    data, nodes, edges, adjacency = load_graph(input_path)
    crown_jewels = set(data.get("crown_jewels", []))

    paths = find_paths(adjacency, "internet", crown_jewels)
    scored = [
        {
            "score": score_path(path),
            "nodes": path_to_nodes(path),
            "edges": path
        }
        for path in paths
    ]

    critical_paths = sorted(
        [path for path in scored if path["score"] >= 10],
        key=lambda item: item["score"],
        reverse=True
    )

    (output_dir / "attack-paths.json").write_text(json.dumps(critical_paths, indent=2), encoding="utf-8")
    (output_dir / "cloud-risk-graph.dot").write_text(generate_dot(nodes, edges, critical_paths), encoding="utf-8")
    (output_dir / "attack-path-report.md").write_text(generate_markdown(nodes, critical_paths), encoding="utf-8")

    print(f"[+] Nodes: {len(nodes)}")
    print(f"[+] Edges: {len(edges)}")
    print(f"[+] Crown jewels: {len(crown_jewels)}")
    print(f"[+] Critical attack paths: {len(critical_paths)}")
    print(f"[+] Output directory: {output_dir}")

    for item in critical_paths:
        labels = " -> ".join(nodes[node_id]["label"] for node_id in item["nodes"])
        print(f"- score={item['score']} | {labels}")

    if critical_paths:
        sys.exit(1)

if __name__ == "__main__":
    main()
