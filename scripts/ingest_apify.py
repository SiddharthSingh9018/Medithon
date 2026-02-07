import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.services.ingestion_apify import ingest_apify_dataset
from app.core.config import APIFY_DATASET_ID

if __name__ == "__main__":
    dataset_id = APIFY_DATASET_ID
    if not dataset_id:
        raise SystemExit("APIFY_DATASET_ID is missing")
    print(ingest_apify_dataset(dataset_id))
