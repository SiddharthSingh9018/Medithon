from app.core.data_files import load_perception_rules
from app.store import STORE, PerceptionSignal

RULES = load_perception_rules()


def derive_perception_for_mentions(limit: int = 200):
    created = 0
    mentions = list(STORE.mentions.values())[:limit]
    for m in mentions:
        text = m.raw_text.lower()
        ctx = STORE.contexts.get(m.mention_id)
        label = _classify(text)
        perception = _derive_from_context(ctx)
        ps = STORE.perceptions.get(m.mention_id)
        if ps is None:
            ps = PerceptionSignal(mention_id=m.mention_id)
        _apply_signal(ps, label)
        _apply_context_perception(ps, perception)
        STORE.set_perception(ps)
        created += 1
    return {"status": "ok", "processed": created}


def _classify(text: str):
    for label, payload in RULES.items():
        for p in payload.get("match", []):
            if p in text:
                return label
    return "neutral"


def _apply_signal(ps: PerceptionSignal, label: str):
    payload = RULES.get(label)
    if not payload:
        return
    fields = payload.get("fields", {})
    for key, value in fields.items():
        setattr(ps, key, value)


def _derive_from_context(ctx):
    if ctx is None:
        return {}
    keywords = set(ctx.keywords)
    result = {
        "perceived_effectiveness": "neutral",
        "emotion_primary": "neutral",
        "expectation_alignment": "unclear",
    }
    if "doesn't work" in keywords or "doesnt work" in keywords or "no relief" in keywords or "did nothing" in keywords:
        result["perceived_effectiveness"] = "low"
        result["emotion_primary"] = "frustration"
        result["expectation_alignment"] = "failed"
    elif "works" in keywords or "worked" in keywords or "helped" in keywords:
        result["perceived_effectiveness"] = "high"
        result["emotion_primary"] = "relief"
        result["expectation_alignment"] = "met"
    return result


def _apply_context_perception(ps: PerceptionSignal, perception: dict):
    for key, value in perception.items():
        setattr(ps, key, value)
