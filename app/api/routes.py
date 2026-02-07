from fastapi import APIRouter
from datetime import datetime
from app.services.aggregation import get_timeline, get_perception_counts
from app.services.context_extraction import extract_context_for_mentions
from app.services.ingestion_apify import ingest_apify_dataset
from app.services.perception_derivation import derive_perception_for_mentions
from app.store import STORE
from app.schemas.mention import MentionCreate

router = APIRouter(prefix="/api")

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/store/load")
def store_load():
    return {"loaded": STORE.load()}

@router.post("/store/save")
def store_save():
    path = STORE.save()
    return {"saved": True, "path": path}

@router.post("/mentions")
def create_mention(payload: MentionCreate):
    ts = payload.timestamp or datetime.utcnow()
    mention = STORE.add_mention(
        drug_id=payload.drug_id,
        raw_text=payload.raw_text,
        timestamp=ts,
        platform=payload.platform,
        language=payload.language,
        location_raw=payload.location_raw,
    )
    return {"mention_id": mention.mention_id}

@router.post("/ingest/apify")
def ingest_apify(dataset_id: str):
    return ingest_apify_dataset(dataset_id)

@router.post("/process/context")
def process_context(limit: int = 200):
    return extract_context_for_mentions(limit)

@router.post("/process/perception")
def process_perception(limit: int = 200):
    return derive_perception_for_mentions(limit)

@router.get("/timeline/{drug_id}")
def timeline(drug_id: int, window_days: int = 7):
    return get_timeline(drug_id, window_days)

@router.get("/perception/{drug_id}")
def perception(drug_id: int):
    return get_perception_counts(drug_id)
