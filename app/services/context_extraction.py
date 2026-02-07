import re
from app.store import STORE, Context

SYMPTOM_LEXICON = {
    "fever": "systemic",
    "headache": "pain",
    "nausea": "gastrointestinal",
    "vomiting": "gastrointestinal",
    "dizziness": "neurological",
    "rash": "dermatological",
}

EFFECTIVENESS_KEYWORDS = [
    "works",
    "worked",
    "doesn't work",
    "doesnt work",
    "no relief",
    "helped",
    "did nothing",
]


def extract_context_for_mentions(limit: int = 200):
    processed = 0
    mentions = list(STORE.mentions.values())[:limit]
    for m in mentions:
        text = m.raw_text.lower()
        symptoms_found = []
        keywords_found = []
        for symptom, classification in SYMPTOM_LEXICON.items():
            if symptom in text:
                s = STORE.get_or_create_symptom(symptom, classification)
                STORE.link_symptom(m.mention_id, s.symptom_id)
                symptoms_found.append(symptom)
        for kw in EFFECTIVENESS_KEYWORDS:
            if kw in text:
                keywords_found.append(kw)
        STORE.set_context(Context(
            mention_id=m.mention_id,
            symptoms=symptoms_found,
            keywords=keywords_found,
        ))
        processed += 1
    return {"status": "ok", "processed": processed}
