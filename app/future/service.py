from __future__ import annotations

from typing import Dict, List

from app.future.analysis import (
    classify_belief_stability,
    classify_emotion_pattern,
    detect_communication_gap,
    diagnose_propagation_risk,
)
from app.future.graph import build_interaction_graph
from app.future.union_find import UnionFind
from app.store import STORE


def summarize(drug_id: int, node_mode: str = "mention") -> Dict:
    nodes, edges = build_interaction_graph(drug_id, node_mode=node_mode)

    if not nodes:
        return {
            "drug_id": drug_id,
            "clusters": [],
            "notes": ["No mentions available for this drug."],
        }

    uf = UnionFind(list(nodes.keys()))
    for e in edges:
        uf.union(e.source_node, e.target_node)

    components: Dict[str, List[str]] = {}
    for node_id in nodes.keys():
        root = uf.find(node_id)
        components.setdefault(root, []).append(node_id)

    clusters = []
    component_beliefs = []
    has_bridges = len(edges) > 0

    for root, node_ids in components.items():
        node_objs = [nodes[nid] for nid in node_ids]
        dominant_belief = _dominant_beliefs(node_objs)
        component_beliefs.append(dominant_belief[0] if dominant_belief else "neutral")

        stability = classify_belief_stability(node_objs)
        emotion_pattern = classify_emotion_pattern(node_objs)
        internal_density = _density_label(len(node_ids), _internal_edges(node_ids, edges))
        external_connectivity = _external_label(node_ids, edges)
        risk = diagnose_propagation_risk(internal_density, external_connectivity, emotion_pattern, stability)

        clusters.append({
            "cluster_id": f"cluster:{root}",
            "dominant_beliefs": dominant_belief,
            "belief_stability": stability,
            "propagation_risk": risk,
            "emotion_pattern": emotion_pattern,
            "internal_density": internal_density,
            "external_connectivity": external_connectivity,
            "interpretation": _interpretation(stability, external_connectivity, emotion_pattern),
            "node_ids": node_ids,
        })

    gap = detect_communication_gap(component_beliefs, has_bridges)

    drug = STORE.drugs.get(drug_id)
    drug_name = drug.drug_name if drug else str(drug_id)

    return {
        "drug": drug_name,
        "clusters": clusters,
        "communication_gap": gap,
        "notes": [
            "Directional diagnostics only; no medical, causal, or outcome prediction.",
            "Uses anonymized interaction structure and existing perception signals.",
        ],
    }


def _dominant_beliefs(nodes) -> List[str]:
    flags = {
        "safety_doubt": 0,
        "effectiveness_doubt": 0,
        "legitimacy_doubt": 0,
        "placebo_failure": 0,
    }
    for n in nodes:
        if n.safety_doubt:
            flags["safety_doubt"] += 1
        if n.effectiveness_doubt:
            flags["effectiveness_doubt"] += 1
        if n.legitimacy_doubt:
            flags["legitimacy_doubt"] += 1
        if n.placebo_failure:
            flags["placebo_failure"] += 1
    ordered = sorted(flags.items(), key=lambda x: x[1], reverse=True)
    return [k for k, v in ordered if v > 0] or ["neutral"]


def _internal_edges(node_ids: List[str], edges) -> int:
    node_set = set(node_ids)
    total = 0
    for e in edges:
        if e.source_node in node_set and e.target_node in node_set:
            total += e.weight
    return int(total)


def _density_label(node_count: int, internal_edges: int) -> str:
    if node_count <= 1:
        return "low"
    if internal_edges >= node_count:
        return "high"
    if internal_edges > 0:
        return "medium"
    return "low"


def _external_label(node_ids: List[str], edges) -> str:
    node_set = set(node_ids)
    external = 0
    for e in edges:
        if (e.source_node in node_set and e.target_node not in node_set) or (e.target_node in node_set and e.source_node not in node_set):
            external += e.weight
    if external >= 5:
        return "high"
    if external >= 1:
        return "medium"
    return "low"


def _interpretation(stability: str, external: str, emotion_pattern: str) -> str:
    if stability == "internally_reinforcing" and external in {"low"}:
        return "This belief is internally reinforcing but structurally contained."
    if external in {"high", "medium"} and emotion_pattern in {"emotion_spilling", "high_volatility"}:
        return "This belief shows cross-group exposure with elevated emotional intensity."
    if stability == "contested":
        return "Belief signals are contested with mixed perceptions inside the cluster."
    return "Belief signals are present but structurally sparse."
