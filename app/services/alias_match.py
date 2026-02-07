from typing import Optional
from app.store import STORE


def resolve_drug_id_from_text(text: str) -> Optional[int]:
    text_l = text.lower()
    for drug in STORE.drugs.values():
        if drug.drug_name.lower() in text_l:
            return drug.drug_id
        for alias in (drug.aliases or []):
            if alias.lower() in text_l:
                return drug.drug_id
    return None
