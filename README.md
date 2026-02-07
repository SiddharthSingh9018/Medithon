# Pharma Perception Monitoring System

## Problem Statement

Pharmaceutical companies often detect perception failures too late—after misinformation has spread, trust has eroded, or sales have already declined.

Meanwhile, patients and healthcare professionals continuously discuss medicines online. These discussions generate real-time signals about safety, effectiveness, and trust, yet they remain largely unstructured and under-analyzed.

This project addresses that gap by converting public drug discourse into structured perception intelligence.

---

## Core Idea

The system treats online drug discussions as **belief signals**, not medical truth.

It explicitly separates:

- **Evidence** — what people say  
- **Context** — symptoms, keywords, framing  
- **Interpretation** — perceived safety, effectiveness, legitimacy, trust  

By keeping these layers distinct, the system reconstructs how public perception evolves over time without conflating sentiment with pharmacological reality.

---

## System Overview

An end-to-end pipeline for perception monitoring:

### 1. Data Ingestion
Public posts mentioning drugs (e.g., *Crocin*) are collected from platforms such as Reddit and Twitter.

### 2. Evidence Storage
Raw mentions are stored **without interpretation**, including:
- timestamp  
- platform  
- referenced symptoms (e.g., fever, headache)

### 3. Perception Analysis
Each mention is analyzed to extract directional signals:
- emotional tone  
- perceived effectiveness  
- perceived side effects  
- safety and legitimacy beliefs  
- expectation / placebo alignment  

### 4. Aggregation
Signals are aggregated across time (and optionally geography) to detect:
- trends  
- inflection points  
- anomalous belief shifts  

### 5. API Layer
A FastAPI backend exposes analytical queries (not raw tables) to the frontend.

### 6. Dashboard
A lightweight frontend visualizes:
- perception trends  
- narrative drivers  
- cross-drug comparisons  

---

## Core Data Objects

- **Drug** — pharmaceutical product being tracked  
- **Mention** — single public reference to a drug  
- **Symptom** — bodily state referenced (fever, headache, nausea)  
- **PerceptionSignal** — multi-dimensional belief attributes (safety, effectiveness, trust)  
- **KeywordAssociation** — contextual terms influencing perception  
- **TemporalAggregate** — time-bucketed perception summaries  

---

## What the Dashboard Answers

- Is public perception improving or deteriorating?
- Are negative beliefs driven by side-effect fear or perceived inefficacy?
- Is misinformation emerging around safety or legitimacy?
- How does one brand compare against competitors?
- When did trust or expectation collapse begin?

---

## Tech Stack

- **Backend:** FastAPI  
- **NLP Analysis:** Python, NLTK / VADER  
- **Database:** SQL  
- **Frontend:** HTML / CSS / JavaScript  
  - *(Streamlit supported for rapid prototyping)*  

---

## Design Principles

- Evidence before interpretation  
- Perception ≠ pharmacology  
- Aggregate analysis only (no user profiling)  
- Interpretable, baseline NLP suitable for hackathon constraints  

---

## Limitations

- Perception signals are directional, not clinical diagnoses  
- Location data may be incomplete or inferred  
- Models prioritize interpretability over sophistication  

---

## Intended Use Cases

Designed for:
- public-health monitoring  
- misinformation detection  
- communication strategy alignment  
- early perception-risk identification  

Not intended for:
- targeted advertising  
- individual-level user analysis  
- medical or regulatory claims  

---

## One-Line Summary

A perception-monitoring system that converts unstructured public drug discussions into structured early-warning signals for trust, safety, and effectiveness narratives.
