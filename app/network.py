from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


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
    dominant_perception: str
    internal_density: str
    external_connectivity: str


@dataclass
class BeliefTrajectorySignal:
    drug_id: int
    narrative: str
    notes: List[str]
