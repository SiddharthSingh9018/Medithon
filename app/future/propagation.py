from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from app.store import STORE


# This module diagnoses belief stability and propagation risk by analyzing
# interaction structure and emotional containment across discussion clusters,
# without user profiling or outcome prediction.

def build_interaction_graph(drug_id: int) -> Tuple[Dict[str, List[str]], Dict[str, int]]:
    # Nodes are discussion entities (thread or mention). Edges are reply-like links.
    nodes: Dict[str, List[str]] = {}
    edges: Dict[str, int] = {}

    def node_id_for_mention(m):
        if m.thread_id:
            return f"thread:{m.thread_id}"
        return f"mention:{m.mention_id}"

    mentions = [m for m in STORE.mentions.values() if m.drug_id == drug_id]
    for m in mentions:
        nid = node_id_for_mention(m)
        nodes.setdefault(nid, []).append(str(m.mention_id))

        if m.parent_mention_id:
            parent = STORE.mentions.get(m.parent_mention_id)
            if parent:
                src = node_id_for_mention(parent)
                dst = nid
                key = f"{src}->{dst}"
                edges[key] = edges.get(key, 0) + 1

    return nodes, edges


def _belief_label(mention_id: int) -> str:
    p = STORE.perceptions.get(mention_id)
    if not p:
        return "neutral"
    eff = p.perceived_effectiveness or "neutral"
    emo = p.emotion_primary or "neutral"
    legit = p.perceived_legitimacy or "neutral"
    return f"{eff}:{emo}:{legit}"


def derive_belief_clusters(nodes: Dict[str, List[str]], edges: Dict[str, int]):
    # Clusters are grouped by dominant belief pattern within each node.
    clusters = []
    for node_id, mention_ids in nodes.items():
        labels = [_belief_label(int(mid)) for mid in mention_ids]
        dominant = _dominant(labels)

        internal_density = _density_label(len(mention_ids), _internal_edge_count(node_id, edges))
        external_exposure = _external_label(node_id, edges)
        emotional_intensity = _emotion_label(mention_ids)

        clusters.append({
            "cluster_id": f"cluster:{node_id}",
            "node_id": node_id,
            "dominant_belief": dominant,
            "internal_coherence": internal_density,
            "external_exposure": external_exposure,
            "emotional_intensity": emotional_intensity,
            "mention_ids": mention_ids,
        })
    return clusters


def classify_belief_stability(cluster) -> str:
    if cluster["internal_coherence"] in {"high", "medium"} and cluster["external_exposure"] in {"low", "none"}:
        return "structurally_contained"
    if cluster["external_exposure"] in {"medium", "high"}:
        return "bridge_crossing"
    return "isolated"


def detect_communication_gaps(clusters) -> bool:
    beliefs = {c["dominant_belief"] for c in clusters}
    if len(beliefs) <= 1:
        return False
    weak_links = all(c["external_exposure"] in {"none", "low"} for c in clusters)
    return weak_links


def classify_emotion_pattern(cluster) -> str:
    intensity = cluster["emotional_intensity"]
    if intensity == "high":
        return "high_volatility"
    if intensity == "medium":
        return "emotion_spilling"
    return "emotion_contained"


def diagnose_propagation_risk(cluster) -> str:
    if cluster["external_exposure"] in {"high", "medium"} and cluster["emotional_intensity"] in {"high", "medium"}:
        return "high_amplification_likelihood"
    if cluster["external_exposure"] in {"medium"}:
        return "moderate_spread_potential"
    return "low_propagation_risk"


def summarize(drug_id: int):
    nodes, edges = build_interaction_graph(drug_id)
    clusters = derive_belief_clusters(nodes, edges)

    results = []
    for c in clusters:
        results.append({
            "drug_id": drug_id,
            "cluster_id": c["cluster_id"],
            "dominant_belief": c["dominant_belief"],
            "belief_stability": classify_belief_stability(c),
            "propagation_risk": diagnose_propagation_risk(c),
            "communication_gap": detect_communication_gaps(clusters),
            "emotion_pattern": classify_emotion_pattern(c),
            "interpretation": _interpret(c),
        })

    return {
        "drug_id": drug_id,
        "clusters": results,
        "notes": [
            "Directional diagnostics only; no medical, causal, or outcome prediction.",
            "Uses anonymized interaction structure and existing perception signals.",
        ],
    }


def _dominant(labels: List[str]) -> str:
    if not labels:
        return "neutral"
    counts: Dict[str, int] = {}
    for l in labels:
        counts[l] = counts.get(l, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[0][0]


def _internal_edge_count(node_id: str, edges: Dict[str, int]) -> int:
    total = 0
    for key, weight in edges.items():
        if key.startswith(f"{node_id}->") and key.split("->", 1)[1] == node_id:
            total += weight
    return total


def _density_label(node_size: int, internal_edges: int) -> str:
    if node_size <= 1:
        return "low"
    if internal_edges >= node_size:
        return "high"
    if internal_edges > 0:
        return "medium"
    return "low"


def _external_label(node_id: str, edges: Dict[str, int]) -> str:
    external = 0
    for key, weight in edges.items():
        src, dst = key.split("->", 1)
        if src == node_id and dst != node_id:
            external += weight
        if dst == node_id and src != node_id:
            external += weight
    if external >= 5:
        return "high"
    if external >= 1:
        return "medium"
    return "none"


def _emotion_label(mention_ids: List[str]) -> str:
    intensities = []
    for mid in mention_ids:
        p = STORE.perceptions.get(int(mid))
        if p and p.emotion_intensity is not None:
            intensities.append(p.emotion_intensity)
    if not intensities:
        return "low"
    if max(intensities) >= 7:
        return "high"
    if max(intensities) >= 4:
        return "medium"
    return "low"


def _interpret(cluster) -> str:
    if cluster["external_exposure"] in {"none", "low"} and cluster["internal_coherence"] in {"high", "medium"}:
        return "Belief is reinforced internally but lacks cross-cluster bridges."
    if cluster["external_exposure"] in {"high", "medium"}:
        return "Belief shows cross-cluster exposure and may travel between groups."
    return "Belief signals are present but structurally sparse."
