from fastapi import APIRouter
from app.future.service import summarize

router = APIRouter(prefix="/api/future")

@router.get("/propagation/{drug_id}")
def propagation(drug_id: int, node_mode: str = "mention"):
    return summarize(drug_id, node_mode=node_mode)
