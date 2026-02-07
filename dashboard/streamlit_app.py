import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")

st.title("Perception Dashboard (Minimal)")

drug_id = st.number_input("Drug ID", min_value=1, value=1)
window_days = st.slider("Window (days)", 1, 60, 7)

if st.button("Load Timeline"):
    resp = requests.get(f"{API_BASE}/timeline/{drug_id}?window_days={window_days}")
    st.json(resp.json())
