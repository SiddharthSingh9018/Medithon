# Future Extension: Propagation Risk & Belief Stability Diagnostic Layer

This extension adds a diagnostic layer that analyzes belief stability and propagation risk using interaction structure, not user identity, persuasion, factual truth, or outcome prediction.

## What It Does
- Models discussions as belief-carrying nodes in an interaction graph
- Detects connected components as belief micro-communities
- Diagnoses belief stability, emotional containment, and communication gaps
- Produces qualitative propagation risk labels only

## What It Does NOT Do
- Identify or profile individuals
- Target or intervene in discourse
- Make medical claims
- Predict outcomes, sales, or clinical truth

## Structural Model
- Nodes are discussion units (mention-level or thread-level)
- Edges are reply relationships that represent potential information flow
- Union-Find identifies connected components for fast, interpretable clustering

## Diagnostics Produced
- Belief stability: internally reinforcing, contested, or structurally contained
- Emotional pattern: contained, spilling, or high volatility
- Propagation risk: low, moderate, or high amplification likelihood
- Communication gaps: when multiple belief groups do not interact

## Removability
- Entirely isolated under `app/future/`
- No changes to production schemas are required
- Can be removed without touching core ingestion or perception logic

## Guardrail
This system models public belief dynamics only. It does not infer medical truth or outcomes.
