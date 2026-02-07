from pydantic import BaseModel
from typing import Optional

class PerceptionSignalCreate(BaseModel):
    mention_id: int
    emotion_primary: Optional[str] = None
    emotion_intensity: Optional[int] = None
    perceived_effectiveness: Optional[str] = None
    expectation_alignment: Optional[str] = None
    perceived_side_effects: Optional[str] = None
    perceived_severity: Optional[str] = None
    long_term_safety_fear: Optional[bool] = False
    perceived_legitimacy: Optional[str] = None
    brand_trust: Optional[str] = None
    regulatory_belief: Optional[str] = None
    dosage_confusion: Optional[bool] = False
    self_medication_signal: Optional[bool] = False
    placebo_activation_likelihood: Optional[str] = None
