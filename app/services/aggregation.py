from datetime import datetime, timedelta
from collections import Counter
from app.store import STORE


def get_timeline(drug_id: int, window_days: int = 7):
    since = datetime.utcnow() - timedelta(days=window_days)
    mentions = [m for m in STORE.mentions.values() if m.drug_id == drug_id and m.timestamp >= since]
    counts = Counter()
    for m in mentions:
        p = STORE.perceptions.get(m.mention_id)
        if p:
            label = p.emotion_primary or "neutral"
            counts[label] += 1
    return {"drug_id": drug_id, "window_days": window_days, "distribution": counts}


def get_perception_counts(drug_id: int):
    counts = Counter()
    for m in STORE.mentions.values():
        if m.drug_id != drug_id:
            continue
        p = STORE.perceptions.get(m.mention_id)
        if not p:
            continue
        label = p.perceived_effectiveness or "neutral"
        counts[label] += 1
    return {"drug_id": drug_id, "perception_counts": counts}
