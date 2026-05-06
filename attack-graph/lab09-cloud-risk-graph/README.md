# Lab 09 — Attack Path / Cloud Risk Graph

This lab builds a cloud attack graph from a simple asset inventory.

## Input

```txt
attack-graph/lab09-cloud-risk-graph/data/cloud-assets.json
```

The input describes cloud assets and risky relationships between them.

## Run

```bash
python3 scripts/build-attack-graph.py attack-graph/lab09-cloud-risk-graph/data/cloud-assets.json
```

## Output

```txt
attack-graph/lab09-cloud-risk-graph/output/attack-paths.json
attack-graph/lab09-cloud-risk-graph/output/cloud-risk-graph.dot
attack-graph/lab09-cloud-risk-graph/output/attack-path-report.md
```

## Render graph locally

```bash
dot -Tpng attack-graph/lab09-cloud-risk-graph/output/cloud-risk-graph.dot \
  -o attack-graph/lab09-cloud-risk-graph/output/cloud-risk-graph.png
```

## What this proves

- Cloud asset modeling
- Attack path analysis
- Detection of chained cloud risks
- Security graph thinking
- Executive-style risk reporting
