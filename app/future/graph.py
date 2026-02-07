from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from app.future.models import SocialNode, SocialEdge
from app.store import STORE


def build_interaction_graph(drug_id: int, window_minutes: int = 60) -> Tuple[Dict[str, SocialNode], List[SocialEdge]]:
    # Prototype graph: each mention becomes an anonymized node.
    # Edges are created between temporally adjacent mentions on the same platform.
    mentions = [m for m in STORE.mentions.values() if m.drug_id == drug_id]
    mentions.sort(key=lambda m: m.timestamp)

    nodes: Dict[str, SocialNode] = {}
    edges: List[SocialEdge] = []

    for m in mentions:
        node_id = f"{m.platform}:{m.mention_id}"
        if node_id not in nodes:
            nodes[node_id] = SocialNode(
                node_id=node_id,
                platform=m.platform,
                activity_level="single",
                influence_proxy=None,
            )

    for i in range(1, len(mentions)):
        prev = mentions[i - 1]
        cur = mentions[i]
        if prev.platform != cur.platform:
            continue
        if cur.timestamp - prev.timestamp > timedelta(minutes=window_minutes):
            continue
        source = f"{prev.platform}:{prev.mention_id}"
        target = f"{cur.platform}:{cur.mention_id}"
        edges.append(SocialEdge(
            source_node=source,
            target_node=target,
            interaction_type="adjacent",
            weight=1.0,
        ))

    return nodes, edges
