import streamlit as st
import json
import os
import matplotlib.pyplot as plt
from ibm_watsonx_ai.foundation_models import Model

API_KEY = "bnMrxXM9l9IpR0HwuHaqHvubXmxnBm4v2sHBnKGKgUvD"
PROJECT_ID = "f942fa84-855c-4ffe-8084-57598f06cd7d"
URL = "https://us-south.ml.cloud.ibm.com"

credentials = {
    "apikey": API_KEY,
    "url": URL
}

model = Model(
    model_id="ibm/granite-3-8b-instruct",
    credentials=credentials,
    project_id=PROJECT_ID
)

# ----------------------------
# Cache AI calls
# ----------------------------
@st.cache_data(show_spinner=False)
def generate_ai_response(prompt):
    return model.generate_text(prompt=prompt)

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

# ----------------------------
# Load datasets
# ----------------------------
with open(os.path.join(DATASET_DIR, "risk_scores.json")) as f:
    scores = json.load(f)

with open(os.path.join(DATASET_DIR, "recommendations.json")) as f:
    recommendations = json.load(f)

with open(os.path.join(DATASET_DIR, "migration_decisions.json")) as f:
    decisions = json.load(f)

# ----------------------------
# Sort once globally
# ----------------------------
sorted_scores = sorted(scores["scores"], key=lambda x: x["score"], reverse=True)

# ----------------------------
# Theme
# ----------------------------
st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #071129;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------
st.title("Watsonx AI Migration Executive Control Center")

# ----------------------------
# KPI Cards
# ----------------------------
cols = st.columns(len(sorted_scores))

for i, item in enumerate(sorted_scores):
    score = item["score"]

    if score >= 90:
        color = "#ff1a1a"
    elif score >= 70:
        color = "#ff9900"
    else:
        color = "#009900"

    with cols[i]:
        st.markdown(f"""
        <div style="
            padding:15px;
            border-radius:10px;
            background-color:{color};
            color:white;
            text-align:center;
            font-weight:bold;
            min-height:90px;">
            <div style='font-size:16px'>{item["application"]}</div>
            <div style='font-size:30px'>{score}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Charts Row 1
# ----------------------------
left, right = st.columns(2)

apps = [x["application"] for x in sorted_scores]
vals = [x["score"] for x in sorted_scores]

with left:
    fig, ax = plt.subplots(figsize=(7, 4))

    colors = [
        "red" if v >= 90 else "orange" if v >= 70 else "green"
        for v in vals
    ]

    ax.bar(apps, vals, color=colors)
    ax.set_facecolor("#111827")
    fig.patch.set_facecolor("#111827")
    ax.tick_params(axis='x', colors='white', rotation=30)
    ax.tick_params(axis='y', colors='white')

    for spine in ax.spines.values():
        spine.set_color("white")

    ax.set_title("Migration Risk Portfolio", color="white")
    st.pyplot(fig)

with right:
    fig2, ax2 = plt.subplots(figsize=(7, 4))

    dependency_counts = [
        len(next(r["dependencies"] for r in recommendations["recommendations"] if r["application"] == app))
        for app in apps
    ]

    ax2.barh(apps, dependency_counts, color="skyblue")
    ax2.set_facecolor("#111827")
    fig2.patch.set_facecolor("#111827")
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    for spine in ax2.spines.values():
        spine.set_color("white")

    ax2.set_title("Dependency Criticality", color="white")
    st.pyplot(fig2)

# ----------------------------
# Charts Row 2
# ----------------------------
left2, right2 = st.columns(2)

with left2:
    fig3, ax3 = plt.subplots(figsize=(7, 4))

    timeline_apps = list(reversed(apps))
    timeline_vals = list(range(1, len(timeline_apps)+1))

    ax3.barh(timeline_apps, timeline_vals, color=["green","limegreen","gold","orange","red"])
    ax3.set_facecolor("#111827")
    fig3.patch.set_facecolor("#111827")
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')

    for spine in ax3.spines.values():
        spine.set_color("white")

    ax3.set_title("Migration Execution Timeline", color="white")
    st.pyplot(fig3)

with right2:
    st.subheader("AI Recommendations")

    for rec in recommendations["recommendations"]:
        st.markdown(f"**{rec['application']}**")
        for item in rec["recommendations"][:2]:
            st.markdown(f"• {item}")

# ----------------------------
# AI Narrative
# ----------------------------
st.subheader("AI Migration Narrative")

granite_output = """
FinanceApp remains highest migration concern due to Oracle DB and SAP connector dependency density.

BillingApp requires staged migration because of revenue-system exposure.

ReportingApp and CitrixAccessGateway fit earlier migration waves.

Authentication-heavy systems require rollback readiness before production cutover.
"""

st.markdown(f"""
<div style='background-color:#0b1f3a;
            padding:20px;
            border-radius:10px;
            color:white;
            font-size:16px;
            line-height:1.8'>
{granite_output}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Blast Radius Chain
# ----------------------------
st.subheader("Blast Radius Impact Chain")

critical_app = sorted_scores[0]["application"]

critical_rec = next(
    r for r in recommendations["recommendations"]
    if r["application"] == critical_app
)

chain = [critical_app] + critical_rec["dependencies"]

chain_html = " → ".join([
    f"<span style='padding:10px 15px;background-color:{'red' if i==0 else '#1f77b4'};color:white;border-radius:8px;font-weight:bold'>{x}</span>"
    for i, x in enumerate(chain)
])

st.markdown(chain_html, unsafe_allow_html=True)

# ----------------------------
# Cloud Target Decision
# ----------------------------
st.subheader("Cloud Target Decision")

for item in decisions["decisions"]:
    color = "red" if item["decision"] == "HOLD" else "orange" if item["decision"] == "CONDITIONAL" else "green"

    st.markdown(f"""
    <div style='padding:10px;margin:5px;border-radius:8px;background-color:{color};color:white;font-weight:bold'>
    {item["application"]} → {item["decision"]}
    </div>
    """, unsafe_allow_html=True)

# ----------------------------
# Executive Summary
# ----------------------------
st.subheader("Executive Summary")

critical = len([x for x in sorted_scores if x["score"] >= 90])
hold = len([x for x in decisions["decisions"] if x["decision"] == "HOLD"])
ready = len([x for x in decisions["decisions"] if x["decision"] == "READY"])

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Critical Portfolio", critical)

with c2:
    st.metric("Migration Hold Zone", hold)

with c3:
    st.metric("Ready Wave", ready)

# ----------------------------
# Live AI Application Analysis
# ----------------------------
st.subheader("Live AI Application Analysis")

selected_app = st.selectbox(
    "Select application for AI migration reasoning",
    apps
)

selected_score = next(x["score"] for x in sorted_scores if x["application"] == selected_app)

selected_rec = next(r for r in recommendations["recommendations"] if r["application"] == selected_app)

dependencies = ", ".join(selected_rec["dependencies"])

decision = next(d["decision"] for d in decisions["decisions"] if d["application"] == selected_app)

prompt = f"""
You are an enterprise migration architect.

Application: {selected_app}
Risk score: {selected_score}
Dependencies: {dependencies}
Decision: {decision}

Return exactly 3 short bullets:
- migration priority
- dependency risk
- migration action
"""

with st.spinner("Granite generating migration reasoning..."):
    ai_response = generate_ai_response(prompt)

clean_lines = [line.strip() for line in ai_response.split("\n") if line.strip().startswith("-")]

if len(clean_lines) == 0:
    clean_lines = [
        f"- {selected_app} requires migration control due to risk score {selected_score}",
        f"- Critical dependencies include {dependencies}",
        f"- Recommended migration decision is {decision}"
    ]

ai_response = "<br>".join(clean_lines[:3])

st.markdown(f"""
<div style='background-color:#071633;
            padding:20px;
            border-radius:10px;
            color:white;
            font-size:16px;
            line-height:1.8'>
{ai_response}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Architecture Footer
# ----------------------------
st.caption("Architecture: Static migration portfolio → Watsonx reasoning → executive decision dashboard")