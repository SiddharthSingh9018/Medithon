from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Tuple

from app.future.models import SocialEdge, SocialNode
from app.store import STORE


def build_interaction_graph(drug_id: int, node_mode: str = "mention") -> Tuple[Dict[str, SocialNode], List[SocialEdge]]:
    mentions = [m for m in STORE.mentions.values() if m.drug_id == drug_id]

    nodes: Dict[str, SocialNode] = {}
    edges: List[SocialEdge] = []

    for m in mentions:
        node_id = _node_id(m, node_mode)
        if node_id not in nodes:
            nodes[node_id] = _node_payload(m)

    for m in mentions:
        if not m.parent_mention_id:
            continue
        parent = STORE.mentions.get(m.parent_mention_id)
        if not parent:
            continue
        src = _node_id(parent, node_mode)
        dst = _node_id(m, node_mode)
        if src == dst:
            continue
        edges.append(SocialEdge(
            source_node=src,
            target_node=dst,
            interaction_type="reply",
            weight=1.0,
        ))

    return nodes, edges


def _node_id(m, node_mode: str) -> str:
    if node_mode == "thread" and getattr(m, "thread_id", None):
        return f"thread:{m.thread_id}"
    return f"mention:{m.mention_id}"


def _node_payload(m) -> SocialNode:
    p = STORE.perceptions.get(m.mention_id)

    emotion = None
    intensity = None
    if p is not None:
        emotion = getattr(p, "emotion_primary", None) or getattr(p, "emotion", None)
        intensity = getattr(p, "emotion_intensity", None)

    safety_doubt = bool(getattr(p, "long_term_safety_fear", False))
    if getattr(p, "perceived_safety", None) == "unsafe":
        safety_doubt = True
    effectiveness_doubt = (getattr(p, "perceived_effectiveness", None) == "low")
    legitimacy_doubt = (getattr(p, "perceived_legitimacy", None) == "low") or (getattr(p, "brand_trust", None) == "low") or bool(getattr(p, "legitimacy_doubt", False))
    placebo_failure = (
        (getattr(p, "expectation_alignment", None) == "low")
        or (getattr(p, "placebo_activation_likelihood", None) == "low")
        or (getattr(p, "placebo_expectation_alignment", None) in {"misaligned", "collapsed"})
    )

    sentiment_score = _sentiment_from_emotion(emotion)

    return SocialNode(
        node_id=f"mention:{m.mention_id}",
        timestamp=_ts(m.timestamp),
        text=m.raw_text,
        emotion=emotion,
        emotion_intensity=float(intensity) if intensity is not None else None,
        safety_doubt=safety_doubt,
        effectiveness_doubt=effectiveness_doubt,
        legitimacy_doubt=legitimacy_doubt,
        placebo_failure=placebo_failure,
        sentiment_score=sentiment_score,
    )


def _ts(ts) -> str:
    if isinstance(ts, str):
        return ts
    if isinstance(ts, datetime):
        return ts.isoformat()
    return ""


def _sentiment_from_emotion(emotion: str | None) -> float:
    if not emotion:
        return 0.0
    emotion = emotion.lower()
    if emotion in {"relief", "trust", "satisfied"}:
        return 0.7
    if emotion in {"fear", "doubt", "frustration", "anger"}:
        return -0.7
    return 0.0
