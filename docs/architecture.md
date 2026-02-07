# Architecture Summary

## Layers
1. Evidence: immutable mentions with raw text and metadata
2. Context: symptoms and keywords extracted without causality
3. Interpretation: perception signals representing beliefs
4. Aggregation: time-bucketed dashboards and alerts

## Core Objects
- Drug (anchor)
- Mention (evidence)
- Symptom (context)
- PerceptionSignal (interpretation)
- KeywordAssociation
- TemporalAggregate

## Flow
Ingestion -> Evidence Store -> Context Extraction -> Perception Derivation -> Aggregation -> API -> Dashboard

## Guardrail
This system models public belief about medicines, not pharmacological truth.
