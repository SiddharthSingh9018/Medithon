from fastapi import APIRouter
from app.future.service import future_predictive_summary
from app.future.propagation import summarize

router = APIRouter(prefix="/api/future")

@router.get("/predict/{drug_id}")
def future_predict(drug_id: int):
    return future_predictive_summary(drug_id)

@router.get("/propagation/{drug_id}")
def future_propagation(drug_id: int):
    return summarize(drug_id)
