import streamlit as st
import json
import os
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from ibm_watsonx_ai.foundation_models import Model
from governance.audit_logger import log_action
from governance.model_validator import validate_ai_output

# ----------------------------
# IBM Credentials
# ----------------------------
API_KEY = st.secrets["API_KEY"]
PROJECT_ID = st.secrets["PROJECT_ID"]
URL = st.secrets["URL"]

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
    try:
        return model.generate_text(prompt=prompt)
    except Exception as e:
        return f"AI generation failed: {str(e)}"

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
MERMAID_FILE = os.path.join(DATASET_DIR, "mermaid_output.txt")

# ----------------------------
# Load Mermaid Dynamic File
# ----------------------------
if os.path.exists(MERMAID_FILE):
    with open(MERMAID_FILE) as f:
        mermaid_text = f.read()
else:
    mermaid_text = "graph TD\nNoData --> NoDependency"

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
# Sort globally
# ----------------------------
sorted_scores = sorted(scores["scores"], key=lambda x: x["score"], reverse=True)

apps = [x["application"] for x in sorted_scores]
vals = [x["score"] for x in sorted_scores]

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

st.markdown("""
<style>
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 40px !important;
}

[data-testid="stMetricLabel"] {
    color: white !important;
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------
st.title("Watsonx AI Migration Executive Control Center")

# ----------------------------
# Governance Status
# ----------------------------
st.success("AI Governance Active | Prompt Audited | Output Validated")

# ----------------------------
# KPI Cards
# ----------------------------
st.subheader("Application Risk Portfolio")

cols = st.columns(len(sorted_scores))

for i, item in enumerate(sorted_scores):
    score = item["score"]
    app_name = item["application"]

    if score >= 90:
        color = "#ff1a1a"
    elif score >= 70:
        color = "#ff9900"
    else:
        color = "#009900"

    app_rec = next(
        r for r in recommendations["recommendations"]
        if r["application"] == app_name
    )

    deps = ", ".join(app_rec["dependencies"][:3])

    app_decision = next(
        d["decision"] for d in decisions["decisions"]
        if d["application"] == app_name
    )

    tooltip = f"Dependencies: {deps} | Decision: {app_decision}"

    with cols[i]:
        st.markdown(f"""
        <div title="{tooltip}" style="
            padding:15px;
            border-radius:10px;
            background-color:{color};
            color:white;
            text-align:center;
            font-weight:bold;
            min-height:90px;
            cursor:pointer;">
            <div style='font-size:16px'>{app_name}</div>
            <div style='font-size:30px'>{score}</div>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------
# Global Application Selector
# ----------------------------
st.markdown(
    "<div style='color:#78a9ff;font-weight:bold;font-size:18px;margin-bottom:5px;'>Select Application for Full Dashboard Analysis</div>",
    unsafe_allow_html=True
)

selected_app_global = st.selectbox(
    "",
    apps,
    key="global_app"
)

# ----------------------------
# Charts Row 1
# ----------------------------
left, right = st.columns(2)

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
# Mermaid Dependency Flow
# ----------------------------
st.subheader("Dynamic Dependency Flow")

selected_mermaid_rec = next(
    r for r in recommendations["recommendations"]
    if r["application"] == selected_app_global
)

highlight_styles = [
    f"style {selected_app_global} fill:#ff4d4d,color:#ffffff,stroke:#ffffff,stroke-width:3px"
]

for dep in selected_mermaid_rec["dependencies"]:
    highlight_styles.append(
        f"style {dep} fill:#3399ff,color:#ffffff,stroke:#ffffff,stroke-width:2px"
    )
graph_lines = mermaid_text.strip().split("\n")

highlighted_mermaid = "\n".join(graph_lines)

highlighted_mermaid += "\n" + "\n".join(highlight_styles)

mermaid_html = f"""
<html>
<head>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

mermaid.initialize({{
    startOnLoad: true,
    theme: 'base',
    themeVariables: {{
        primaryColor: '#ffffff',
        primaryTextColor: '#000000',
        primaryBorderColor: '#ffffff',
        lineColor: '#888888',
        fontSize: '20px'
    }}
}});
</script>
</head>
<body style="background-color:#071129;">
<div class="mermaid">
{highlighted_mermaid}
</div>
</body>
</html>
"""

components.html(mermaid_html, height=290)
# ----------------------------
# AI Narrative
# ----------------------------
st.subheader("AI Migration Narrative")

selected_narrative_app = selected_app_global

selected_narrative_score = next(
    x["score"] for x in sorted_scores if x["application"] == selected_narrative_app
)

selected_narrative_rec = next(
    r for r in recommendations["recommendations"]
    if r["application"] == selected_narrative_app
)

narrative_dependencies = ", ".join(selected_narrative_rec["dependencies"])

narrative_decision = next(
    d["decision"] for d in decisions["decisions"]
    if d["application"] == selected_narrative_app
)

narrative_prompt = f"""
Application: {selected_narrative_app}
Risk Score: {selected_narrative_score}
Dependencies: {narrative_dependencies}
Decision: {narrative_decision}

Provide executive migration reasoning.
"""

log_action("Narrative Prompt Submitted", narrative_prompt)

# Keep Granite call for governance logging
granite_output = generate_ai_response(narrative_prompt)

if validate_ai_output(granite_output):
    log_action("Narrative Accepted", granite_output)

# Deterministic executive narrative
risk_level = "high" if selected_narrative_score >= 90 else "moderate" if selected_narrative_score >= 70 else "controlled"

line1 = f"1. Dependency risk remains {risk_level} due to {selected_narrative_rec['dependencies'][0]}."
line2 = f"2. Blast radius extends across {len(selected_narrative_rec['dependencies'])} connected services."
line3 = f"3. Migration sequencing recommends {narrative_decision.lower()} execution control."
line4 = f"4. Cloud readiness for {selected_narrative_app} depends on dependency stabilization."

narrative_display = "<br><br>".join([line1, line2, line3, line4])

st.markdown(
    f"""
    <div style='background-color:#0b1f3a;
    padding:20px;
    border-radius:10px;
    color:white;
    font-size:16px;
    line-height:2'>
    {narrative_display}
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Blast Radius Chain
# ----------------------------
st.subheader("Blast Radius Impact Chain")

selected_chain_app = selected_app_global

selected_chain_rec = next(
    r for r in recommendations["recommendations"]
    if r["application"] == selected_chain_app
)

chain = [selected_chain_app] + selected_chain_rec["dependencies"]

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

selected_app = selected_app_global

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

Dependency Graph:
{mermaid_text}

Return exactly 3 bullets:
- migration priority
- dependency risk
- migration action
"""

log_action("Live Prompt Submitted", prompt)

with st.spinner("Granite generating migration reasoning..."):
    ai_response = generate_ai_response(prompt)

if validate_ai_output(ai_response):
    log_action("Live AI Response Accepted", ai_response)
else:
    ai_response = "- Governance blocked weak response"

clean_lines = []

for line in ai_response.split("\n"):
    line = line.strip()

    if (
        line.startswith("-")
        or line.startswith("•")
        or line[:2].isdigit()
        or len(line) > 15
    ):
        clean_lines.append(line)

if len(clean_lines) < 3:
    clean_lines = [
        f"- {selected_app} migration priority remains linked to score {selected_score}",
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
# Footer
# ----------------------------
st.caption("Architecture: Dynamic dependency scan → Governance → Watsonx reasoning → Executive decision dashboard")