from __future__ import annotations

from typing import Dict

from app.future.graph import build_interaction_graph
from app.future.analysis import cluster_beliefs, analyze_dispersion


def future_predictive_summary(drug_id: int) -> Dict:
    nodes, edges = build_interaction_graph(drug_id)
    clusters = cluster_beliefs(list(nodes.keys()))
    diagnostics, notes = analyze_dispersion(clusters)

    return {
        "drug_id": drug_id,
        "nodes": len(nodes),
        "edges": len(edges),
        "clusters": [c.__dict__ for c in clusters],
        "diagnostics": [d.__dict__ for d in diagnostics],
        "notes": notes,
        "guardrail": "Directional, structural diagnostics only; not medical or causal inference.",
    }
