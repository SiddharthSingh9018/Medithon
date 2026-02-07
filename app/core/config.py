import os
from dotenv import load_dotenv

load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
APIFY_DATASET_ID = os.getenv("APIFY_DATASET_ID", "")
STORE_PATH = os.getenv("STORE_PATH", os.path.join("data", "store.json"))
