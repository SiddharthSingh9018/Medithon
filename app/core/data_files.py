from pathlib import Path
import json

RULES_PATH = Path(__file__).resolve().parents[2] / "data" / "perception_rules.json"
DRUGS_PATH = Path(__file__).resolve().parents[2] / "data" / "drugs_seed.json"


def load_perception_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_drug_seed():
    with open(DRUGS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
