from collections import Counter
from typing import Dict, List

from app.network import BeliefTrajectorySignal
from app.store import STORE


def analyze_belief_trajectory(drug_id: int) -> Dict:
    # High-level, directional analysis using only aggregate structure
    # This prototype uses in-store perception + context presence as a stand-in
    # for structural intensity and dispersion.
    mentions = [m for m in STORE.mentions.values() if m.drug_id == drug_id]
    perceptions = [STORE.perceptions.get(m.mention_id) for m in mentions]
    perceptions = [p for p in perceptions if p is not None]

    if not perceptions:
        return {
            "drug_id": drug_id,
            "signals": [],
            "notes": ["Insufficient perception data to infer belief trajectory."],
        }

    effectiveness = Counter([(p.perceived_effectiveness or "neutral") for p in perceptions])
    emotions = Counter([(p.emotion_primary or "neutral") for p in perceptions])

    signals: List[BeliefTrajectorySignal] = []
    notes: List[str] = []

    if effectiveness.get("low", 0) > effectiveness.get("high", 0):
        signals.append(BeliefTrajectorySignal(
            drug_id=drug_id,
            narrative="This belief narrative is likely to intensify.",
            notes=["Effectiveness doubt dominates recent perceptions."],
        ))
    if emotions.get("fear", 0) > 0 or emotions.get("doubt", 0) > 0:
        signals.append(BeliefTrajectorySignal(
            drug_id=drug_id,
            narrative="This perception is structurally isolated.",
            notes=["Negative emotions appear without balancing relief signals."],
        ))
    if effectiveness.get("neutral", 0) == len(perceptions):
        notes.append("Belief signals are diffuse; no dominant narrative.")

    return {
        "drug_id": drug_id,
        "signals": [s.__dict__ for s in signals],
        "notes": notes,
        "summary": {
            "effectiveness": effectiveness,
            "emotions": emotions,
        },
    }
