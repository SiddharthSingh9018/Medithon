import requests
from datetime import datetime
from app.core.config import APIFY_API_TOKEN
from app.services.alias_match import resolve_drug_id_from_text
from app.store import STORE

APIFY_API = "https://api.apify.com/v2/datasets"


def ingest_apify_dataset(dataset_id: str, limit: int = 200):
    if not APIFY_API_TOKEN:
        return {"status": "error", "detail": "APIFY_API_TOKEN missing"}

    url = f"{APIFY_API}/{dataset_id}/items?token={APIFY_API_TOKEN}&limit={limit}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    items = resp.json()

    created = 0
    skipped = 0
    for item in items:
        raw_text = item.get("text") or item.get("body") or ""
        if not raw_text:
            skipped += 1
            continue

        drug_id = item.get("drug_id")
        if not drug_id:
            drug_id = resolve_drug_id_from_text(raw_text)
        if not drug_id:
            skipped += 1
            continue

        STORE.add_mention(
            drug_id=drug_id,
            raw_text=raw_text,
            timestamp=_parse_ts(item.get("timestamp")),
            platform=item.get("platform", "unknown"),
            language=item.get("language"),
            location_raw=item.get("location"),
        )
        created += 1

    return {"status": "ok", "created": created, "skipped": skipped}


def _parse_ts(ts):
    if not ts:
        return datetime.utcnow()
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return datetime.utcnow()
