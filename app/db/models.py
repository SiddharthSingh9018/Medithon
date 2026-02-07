from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Drug(Base):
    __tablename__ = "drug"
    drug_id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String(255), nullable=False)
    aliases = Column(JSON, default=list)
    category = Column(String(255), nullable=True)
    tracking_status = Column(String(64), default="active")

    mentions = relationship("Mention", back_populates="drug")

class Mention(Base):
    __tablename__ = "mention"
    mention_id = Column(Integer, primary_key=True, index=True)
    drug_id = Column(Integer, ForeignKey("drug.drug_id"), nullable=False)
    raw_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    platform = Column(String(128), nullable=False)
    language = Column(String(16), nullable=True)
    location_raw = Column(String(255), nullable=True)

    drug = relationship("Drug", back_populates="mentions")
    symptoms = relationship("MentionSymptom", back_populates="mention")
    perception = relationship("PerceptionSignal", back_populates="mention", uselist=False)

class Symptom(Base):
    __tablename__ = "symptom"
    symptom_id = Column(Integer, primary_key=True, index=True)
    symptom_name = Column(String(255), nullable=False, unique=True)
    classification = Column(String(128), nullable=True)

class MentionSymptom(Base):
    __tablename__ = "mention_symptom"
    mention_id = Column(Integer, ForeignKey("mention.mention_id"), primary_key=True)
    symptom_id = Column(Integer, ForeignKey("symptom.symptom_id"), primary_key=True)

    mention = relationship("Mention", back_populates="symptoms")
    symptom = relationship("Symptom")

class PerceptionSignal(Base):
    __tablename__ = "perception_signal"
    mention_id = Column(Integer, ForeignKey("mention.mention_id"), primary_key=True)

    emotion_primary = Column(String(32), nullable=True)
    emotion_intensity = Column(Integer, nullable=True)
    perceived_effectiveness = Column(String(32), nullable=True)
    expectation_alignment = Column(String(32), nullable=True)
    perceived_side_effects = Column(String(255), nullable=True)
    perceived_severity = Column(String(32), nullable=True)
    long_term_safety_fear = Column(Boolean, default=False)
    perceived_legitimacy = Column(String(32), nullable=True)
    brand_trust = Column(String(32), nullable=True)
    regulatory_belief = Column(String(32), nullable=True)
    dosage_confusion = Column(Boolean, default=False)
    self_medication_signal = Column(Boolean, default=False)
    placebo_activation_likelihood = Column(String(32), nullable=True)

    mention = relationship("Mention", back_populates="perception")

class KeywordAssociation(Base):
    __tablename__ = "keyword_association"
    keyword = Column(String(128), primary_key=True)
    drug_id = Column(Integer, ForeignKey("drug.drug_id"), primary_key=True)
    frequency = Column(Integer, default=0)
    dominant_perception_signal = Column(String(64), nullable=True)
    time_window = Column(String(64), primary_key=True)

class TemporalAggregate(Base):
    __tablename__ = "temporal_aggregate"
    drug_id = Column(Integer, ForeignKey("drug.drug_id"), primary_key=True)
    time_window = Column(String(64), primary_key=True)
    mention_count = Column(Integer, default=0)
    perception_distribution = Column(JSON, default=dict)
    symptom_association_strength = Column(JSON, default=dict)
    trust_trend = Column(JSON, default=dict)
    expectation_trend = Column(JSON, default=dict)
