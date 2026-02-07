from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class SocialNode:
    node_id: str
    platform: str
    activity_level: Optional[str] = None
    influence_proxy: Optional[str] = None


@dataclass(frozen=True)
class SocialEdge:
    source_node: str
    target_node: str
    interaction_type: str
    weight: float = 1.0


@dataclass(frozen=True)
class BeliefCluster:
    cluster_id: str
    dominant_belief: str
    internal_coherence: str
    external_exposure: str
    emotional_intensity: str
    node_ids: List[str]


@dataclass(frozen=True)
class FutureDiagnostic:
    code: str
    message: str
    notes: List[str]
