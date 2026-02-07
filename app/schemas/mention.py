from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MentionCreate(BaseModel):
    drug_id: int
    raw_text: str
    timestamp: Optional[datetime] = None
    platform: str
    language: Optional[str] = None
    location_raw: Optional[str] = None
    thread_id: Optional[str] = None
    parent_mention_id: Optional[int] = None
