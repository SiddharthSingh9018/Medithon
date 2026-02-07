from fastapi import FastAPI
from app.api.routes import router as api_router
from app.future.routes import router as future_router
from app.store import STORE

app = FastAPI(
    title="Pharma Market Perception and Misinformation Intelligence",
    version="0.1.0",
)

app.include_router(api_router)
app.include_router(future_router)

@app.on_event("startup")
def load_store():
    STORE.load()
