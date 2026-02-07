import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.core.data_files import load_drug_seed
from app.store import STORE

if __name__ == "__main__":
    data = load_drug_seed()
    for d in data.get("drugs", []):
        if any(drug.drug_name == d["drug_name"] for drug in STORE.drugs.values()):
            continue
        STORE.add_drug(
            drug_name=d["drug_name"],
            aliases=d.get("aliases", []),
            category=d.get("category"),
            tracking_status=d.get("tracking_status", "active"),
        )
    STORE.save()
    print("Seeded drugs")
