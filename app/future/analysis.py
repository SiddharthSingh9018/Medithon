from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, List, Tuple

from app.future.models import BeliefCluster, FutureDiagnostic
from app.store import STORE


def _belief_label(mention_id: int) -> str:
    p = STORE.perceptions.get(mention_id)
    if not p:
        return "neutral"
    eff = p.perceived_effectiveness or "neutral"
    emo = p.emotion_primary or "neutral"
    return f"{eff}:{emo}"


def cluster_beliefs(node_ids: List[str]) -> List[BeliefCluster]:
    # Clusters are grouped by dominant belief label from existing perceptions.
    label_to_nodes: Dict[str, List[str]] = defaultdict(list)
    for node_id in node_ids:
        mention_id = int(node_id.split(":")[-1])
        label_to_nodes[_belief_label(mention_id)].append(node_id)

    clusters: List[BeliefCluster] = []
    for label, nodes in label_to_nodes.items():
        internal = "high" if len(nodes) >= 5 else "medium" if len(nodes) >= 2 else "low"
        external = "low" if len(nodes) >= 5 else "medium"
        emotional = "high" if "fear" in label or "doubt" in label or "frustration" in label else "low"
        clusters.append(BeliefCluster(
            cluster_id=f"cluster:{label}",
            dominant_belief=label,
            internal_coherence=internal,
            external_exposure=external,
            emotional_intensity=emotional,
            node_ids=nodes,
        ))
    return clusters


def analyze_dispersion(clusters: List[BeliefCluster]) -> Tuple[List[FutureDiagnostic], List[str]]:
    diagnostics: List[FutureDiagnostic] = []
    notes: List[str] = []

    if len(clusters) <= 1:
        notes.append("Belief signals are concentrated; dispersion is limited.")
        return diagnostics, notes

    dominant = Counter([c.dominant_belief for c in clusters])
    if len(dominant) > 2:
        diagnostics.append(FutureDiagnostic(
            code="communication_gap_widening",
            message="This communication gap is widening.",
            notes=["Multiple distinct belief clusters with minimal convergence."],
        ))

    isolated = [c for c in clusters if c.external_exposure == "low" and c.internal_coherence in {"high", "medium"}]
    if isolated:
        diagnostics.append(FutureDiagnostic(
            code="belief_isolated",
            message="This perception is structurally isolated.",
            notes=["Clusters show internal reinforcement with low external exposure."],
        ))

    return diagnostics, notes
