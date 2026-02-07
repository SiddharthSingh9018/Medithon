from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SocialNode:
    node_id: str
    timestamp: str
    text: str
    emotion: Optional[str]
    emotion_intensity: Optional[float]
    safety_doubt: bool
    effectiveness_doubt: bool
    legitimacy_doubt: bool
    placebo_failure: bool
    sentiment_score: float


@dataclass(frozen=True)
class SocialEdge:
    source_node: str
    target_node: str
    interaction_type: str
    weight: float = 1.0


@dataclass(frozen=True)
class BeliefCluster:
    cluster_id: str
    node_ids: List[str]
    dominant_belief: str
    internal_coherence: str
    external_exposure: str
    emotional_intensity: str


@dataclass(frozen=True)
class DiagnosticOutput:
    drug: str
    dominant_beliefs: List[str]
    belief_stability: str
    propagation_risk: str
    emotion_pattern: str
    communication_gap: bool
    interpretation: str
