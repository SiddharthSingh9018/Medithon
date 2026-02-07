# Medithon - Pharma Market Perception and Misinformation Intelligence System

This repo contains a minimal, production-grade scaffolding for a perception-focused pharma intelligence system. It models public belief signals and explicitly avoids medical or pharmacological claims.

## What This Is
- Evidence layer: immutable mentions from public sources
- Context layer: symptoms and keywords
- Interpretation layer: perception signals (beliefs, not facts)
- Aggregation layer: temporal signals for dashboards and alerts

## Quick Start
1. Create a Python virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure environment variables:

```powershell
Copy-Item .env.example .env
```

3. Initialize the local in-memory store and seed drugs:

```powershell
python scripts\init_db.py
python scripts\seed_drugs.py
```

4. Run the API:

```powershell
uvicorn app.main:app --reload
```

5. Optional: Run the Streamlit dashboard:

```powershell
streamlit run dashboard\streamlit_app.py
```

## Notes
- This scaffold uses an in-memory store with optional JSON persistence in `data\store.json`.
- If you use spaCy, download a model, for example:

```powershell
python -m spacy download en_core_web_sm
```

## Guardrail
This system models public belief about medicines, not pharmacological truth.
