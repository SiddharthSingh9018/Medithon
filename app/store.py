from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional
import json
import os

from app.core.config import STORE_PATH


@dataclass(frozen=True)
class Drug:
    drug_id: int
    drug_name: str
    aliases: List[str]
    category: Optional[str] = None
    tracking_status: str = "active"


@dataclass(frozen=True)
class Mention:
    mention_id: int
    drug_id: int
    raw_text: str
    timestamp: datetime
    platform: str
    language: Optional[str] = None
    location_raw: Optional[str] = None
    thread_id: Optional[str] = None
    parent_mention_id: Optional[int] = None


@dataclass(frozen=True)
class Symptom:
    symptom_id: int
    symptom_name: str
    classification: Optional[str] = None


@dataclass
class PerceptionSignal:
    mention_id: int
    emotion_primary: Optional[str] = None
    emotion_intensity: Optional[int] = None
    perceived_effectiveness: Optional[str] = None
    expectation_alignment: Optional[str] = None
    perceived_side_effects: Optional[str] = None
    perceived_severity: Optional[str] = None
    long_term_safety_fear: bool = False
    perceived_legitimacy: Optional[str] = None
    brand_trust: Optional[str] = None
    regulatory_belief: Optional[str] = None
    dosage_confusion: bool = False
    self_medication_signal: bool = False
    placebo_activation_likelihood: Optional[str] = None


@dataclass(frozen=True)
class Context:
    mention_id: int
    symptoms: List[str]
    keywords: List[str]


@dataclass
class TemporalAggregate:
    drug_id: int
    time_window: str
    mention_count: int
    perception_distribution: Dict[str, int]
    symptom_association_strength: Dict[str, int]
    trust_trend: Dict[str, int]
    expectation_trend: Dict[str, int]


class Store:
    def __init__(self) -> None:
        self.drugs: Dict[int, Drug] = {}
        self.mentions: Dict[int, Mention] = {}
        self.symptoms: Dict[int, Symptom] = {}
        self.mention_symptoms: Dict[int, List[int]] = {}
        self.contexts: Dict[int, Context] = {}
        self.perceptions: Dict[int, PerceptionSignal] = {}
        self._drug_id = 1
        self._mention_id = 1
        self._symptom_id = 1

    def add_drug(self, drug_name: str, aliases: Optional[List[str]] = None,
                 category: Optional[str] = None, tracking_status: str = "active") -> Drug:
        drug = Drug(
            drug_id=self._drug_id,
            drug_name=drug_name,
            aliases=aliases or [],
            category=category,
            tracking_status=tracking_status,
        )
        self.drugs[self._drug_id] = drug
        self._drug_id += 1
        return drug

    def add_mention(self, drug_id: int, raw_text: str, timestamp: datetime,
                    platform: str, language: Optional[str] = None,
                    location_raw: Optional[str] = None,
                    thread_id: Optional[str] = None,
                    parent_mention_id: Optional[int] = None) -> Mention:
        mention = Mention(
            mention_id=self._mention_id,
            drug_id=drug_id,
            raw_text=raw_text,
            timestamp=timestamp,
            platform=platform,
            language=language,
            location_raw=location_raw,
            thread_id=thread_id,
            parent_mention_id=parent_mention_id,
        )
        self.mentions[self._mention_id] = mention
        self._mention_id += 1
        return mention

    def get_or_create_symptom(self, name: str, classification: Optional[str] = None) -> Symptom:
        for s in self.symptoms.values():
            if s.symptom_name == name:
                return s
        symptom = Symptom(symptom_id=self._symptom_id, symptom_name=name, classification=classification)
        self.symptoms[self._symptom_id] = symptom
        self._symptom_id += 1
        return symptom

    def link_symptom(self, mention_id: int, symptom_id: int) -> None:
        if mention_id not in self.mention_symptoms:
            self.mention_symptoms[mention_id] = []
        if symptom_id not in self.mention_symptoms[mention_id]:
            self.mention_symptoms[mention_id].append(symptom_id)

    def set_perception(self, signal: PerceptionSignal) -> None:
        self.perceptions[signal.mention_id] = signal
    
    def set_context(self, context: Context) -> None:
        self.contexts[context.mention_id] = context

    def save(self, path: Optional[str] = None) -> str:
        path = path or STORE_PATH
        payload = {
            "drugs": [asdict(d) for d in self.drugs.values()],
            "mentions": [asdict(m) for m in self.mentions.values()],
            "symptoms": [asdict(s) for s in self.symptoms.values()],
            "mention_symptoms": self.mention_symptoms,
            "contexts": [asdict(c) for c in self.contexts.values()],
            "perceptions": [asdict(p) for p in self.perceptions.values()],
            "counters": {
                "drug_id": self._drug_id,
                "mention_id": self._mention_id,
                "symptom_id": self._symptom_id,
            },
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=True, default=str)
        return path

    def load(self, path: Optional[str] = None) -> bool:
        path = path or STORE_PATH
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        self.drugs = {d["drug_id"]: Drug(**d) for d in payload.get("drugs", [])}
        self.mentions = {
            m["mention_id"]: Mention(**{**m, "timestamp": datetime.fromisoformat(m["timestamp"])})
            for m in payload.get("mentions", [])
        }
        self.symptoms = {s["symptom_id"]: Symptom(**s) for s in payload.get("symptoms", [])}
        self.mention_symptoms = {int(k): v for k, v in payload.get("mention_symptoms", {}).items()}
        self.contexts = {c["mention_id"]: Context(**c) for c in payload.get("contexts", [])}
        self.perceptions = {p["mention_id"]: PerceptionSignal(**p) for p in payload.get("perceptions", [])}
        counters = payload.get("counters", {})
        self._drug_id = counters.get("drug_id", max(self.drugs.keys(), default=0) + 1)
        self._mention_id = counters.get("mention_id", max(self.mentions.keys(), default=0) + 1)
        self._symptom_id = counters.get("symptom_id", max(self.symptoms.keys(), default=0) + 1)
        return True


STORE = Store()
