from fastapi import FastAPI
from app.store import STORE
from app.api.routes import router as api_router

app = FastAPI(
    title="Pharma Market Perception and Misinformation Intelligence",
    version="0.1.0",
)

app.include_router(api_router)

@app.on_event("startup")
def load_store():
    STORE.load()
