Problem Statement
Pharma companies often discover perception issues too late—after misinformation spreads, trust erodes, or sales decline.
Meanwhile, patients and healthcare professionals continuously discuss medicines online, creating real‑time signals that are rarely captured systematically.

This tool monitors that discourse to detect:

misinformation (e.g., false safety claims),

perceived ineffectiveness,

emerging side‑effect narratives,

expectation and trust collapse.

Core Idea
The system treats online drug discussions as a belief signal, not medical truth.

It separates:

raw evidence (what people say),

context (symptoms, keywords),

interpretation (perceived safety, effectiveness, trust),

and reconstructs how public perception evolves over time.

System Overview
End‑to‑end pipeline:

Data Ingestion
Public posts mentioning drugs (e.g., Crocin) are collected from platforms like Reddit and Twitter.

Evidence Storage
Raw mentions, timestamps, platforms, and referenced symptoms (e.g., fever, headache) are stored without interpretation.

Perception Analysis
Each mention is analyzed to extract:

emotional tone,

perceived effectiveness,

perceived side effects,

legitimacy and safety beliefs,

expectation / placebo alignment.

Aggregation
Beliefs are aggregated across time and (optionally) geography to detect trends and anomalies.

API Layer
FastAPI endpoints expose analytical questions (not raw tables) to the frontend.

Dashboard
A lightweight frontend visualizes trends, drivers, and comparisons between drugs.

Core Data Objects
Drug – pharmaceutical product being tracked

Mention – single public reference to a drug

Symptom – bodily state mentioned (fever, headache, nausea)

PerceptionSignal – multi‑dimensional belief attributes (safety, effectiveness, trust)

KeywordAssociation – contextual terms driving sentiment

TemporalAggregate – time‑bucketed perception summaries

What the Dashboard Answers
Is perception improving or deteriorating?

Are negative beliefs driven by side‑effect fear or perceived inefficacy?

Is misinformation emerging around safety or legitimacy?

How does one brand compare against competitors?

When did trust or expectation collapse begin?

Tech Stack
Backend: FastAPI

Analysis: Python, NLTK / VADER

Database: SQL

Frontend: HTML / CSS / JavaScript (or Streamlit for rapid demo)

Design Principles
Evidence before interpretation

Perception ≠ pharmacology

Aggregate analysis only (no user profiling)

Honest, baseline NLP suitable for hackathon constraints

Limitations
Sentiment and perception signals are directional, not clinical diagnoses

Location data may be incomplete or inferred

Models prioritize interpretability over sophistication

Use Case
Designed for:

public‑health monitoring,

misinformation diagnosis,

communication strategy alignment,

early perception‑risk detection.

Not intended for:

targeted advertising,

individual user analysis,

medical or regulatory claims.

One‑Line Summary
A perception‑monitoring system that turns unstructured public drug discussions into structured early‑warning signals for trust, safety, and effectiveness narratives.
