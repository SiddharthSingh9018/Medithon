from __future__ import annotations

from collections import Counter
from typing import Dict, List, Tuple

from app.future.models import BeliefCluster


def derive_belief_clusters(nodes: Dict[str, object], edges) -> List[BeliefCluster]:
    clusters = []
    for node_id, node in nodes.items():
        dominant = _dominant_belief(node)
        internal = "high"
        external = "low"
        emotional = _emotion_band(node.emotion_intensity)
        clusters.append(BeliefCluster(
            cluster_id=f"cluster:{node_id}",
            node_ids=[node_id],
            dominant_belief=dominant,
            internal_coherence=internal,
            external_exposure=external,
            emotional_intensity=emotional,
        ))
    return clusters


def classify_belief_stability(nodes: List[object]) -> str:
    if not nodes:
        return "isolated"
    flags = [_belief_vector(n) for n in nodes]
    coherence = _coherence_label(flags)
    if coherence == "high":
        return "internally_reinforcing"
    if coherence == "medium":
        return "contested"
    return "structurally_contained"


def classify_emotion_pattern(nodes: List[object]) -> str:
    intensities = [n.emotion_intensity for n in nodes if n.emotion_intensity is not None]
    if not intensities:
        return "emotion_contained"
    spread = max(intensities) - min(intensities)
    if spread >= 0.5:
        return "emotion_spilling"
    if max(intensities) >= 0.7:
        return "high_volatility"
    return "emotion_contained"


def diagnose_propagation_risk(internal_density: str, external_connectivity: str, emotion_pattern: str, coherence: str) -> str:
    if external_connectivity in {"high", "medium"} and emotion_pattern in {"emotion_spilling", "high_volatility"}:
        return "high_amplification_likelihood"
    if external_connectivity in {"medium"}:
        return "moderate_spread_potential"
    if coherence == "internally_reinforcing":
        return "moderate_spread_potential"
    return "low_propagation_risk"


def detect_communication_gap(component_beliefs: List[str], has_bridges: bool) -> bool:
    if len(set(component_beliefs)) <= 1:
        return False
    return not has_bridges


def _dominant_belief(node) -> str:
    beliefs = []
    if node.safety_doubt:
        beliefs.append("safety_doubt")
    if node.effectiveness_doubt:
        beliefs.append("effectiveness_doubt")
    if node.legitimacy_doubt:
        beliefs.append("legitimacy_doubt")
    if node.placebo_failure:
        beliefs.append("placebo_failure")
    if not beliefs:
        return "neutral"
    counts = Counter(beliefs)
    return counts.most_common(1)[0][0]


def _belief_vector(node) -> Tuple[int, int, int, int]:
    return (
        1 if node.safety_doubt else 0,
        1 if node.effectiveness_doubt else 0,
        1 if node.legitimacy_doubt else 0,
        1 if node.placebo_failure else 0,
    )


def _coherence_label(flags: List[Tuple[int, int, int, int]]) -> str:
    if not flags:
        return "low"
    counts = Counter(flags)
    top = counts.most_common(1)[0][1]
    ratio = top / len(flags)
    if ratio >= 0.7:
        return "high"
    if ratio >= 0.4:
        return "medium"
    return "low"


def _emotion_band(intensity: float | None) -> str:
    if intensity is None:
        return "low"
    if intensity >= 0.7:
        return "high"
    if intensity >= 0.4:
        return "medium"
    return "low"
