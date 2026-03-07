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

# ----------------------------
# Build dynamic Granite prompt
# ----------------------------

sorted_apps = sorted(scores["scores"], key=lambda x: x["score"], reverse=True)

prompt_lines = []

for app in sorted_apps:
    prompt_lines.append(
        f"{app['application']} Risk Score {app['score']}"
    )

granite_prompt = (
    "Enterprise cloud migration portfolio:\n"
    + "\n".join(prompt_lines)
    + "\nExplain migration priority, dependency criticality, blast radius and recommended migration wave."
)

# ----------------------------
# Theme
# ----------------------------
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #071129;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Title
# ----------------------------
st.title("AI Migration Executive Control Center")

# ----------------------------
# KPI Cards
# ----------------------------
cols = st.columns(len(scores["scores"]))

for i, item in enumerate(scores["scores"]):

    score = item["score"]

    if score >= 90:
        color = "#ff1a1a"
    elif score >= 70:
        color = "#ff9900"
    else:
        color = "#009900"

    with cols[i]:
        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:10px;
                background-color:{color};
                color:white;
                text-align:center;
                font-weight:bold;
                min-height:90px;
                display:flex;
                flex-direction:column;
                justify-content:center;
            ">
                <div style='font-size:16px'>{item["application"]}</div>
                <div style='font-size:30px'>{score}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------
# Charts Row 1
# ----------------------------
left, right = st.columns(2)

# ----------------------------
# Risk Portfolio
# ----------------------------
with left:
    fig, ax = plt.subplots(figsize=(7, 4))

    apps = [x["application"] for x in scores["scores"]]
    vals = [x["score"] for x in scores["scores"]]

    colors = []

    for v in vals:
        if v >= 90:
            colors.append("red")
        elif v >= 70:
            colors.append("orange")
        else:
            colors.append("green")

    ax.bar(apps, vals, color=colors)

    ax.set_facecolor("#111827")
    fig.patch.set_facecolor("#111827")

    ax.tick_params(axis='x', colors='white', rotation=30)
    ax.tick_params(axis='y', colors='white')

    for spine in ax.spines.values():
        spine.set_color("white")

    ax.set_title("Migration Risk Portfolio", color="white")

    st.pyplot(fig)

# ----------------------------
# Dependency Criticality
# ----------------------------
with right:
    fig2, ax2 = plt.subplots(figsize=(7, 4))

    dependency_counts = []

    for item in scores["scores"]:
        app = item["application"]

        dep = next(
            len(r["dependencies"])
            for r in recommendations["recommendations"]
            if r["application"] == app
        )

        dependency_counts.append(dep)

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

# ----------------------------
# Migration Timeline
# ----------------------------
with left2:
    fig3, ax3 = plt.subplots(figsize=(7, 4))

    sorted_apps = sorted(scores["scores"], key=lambda x: x["score"])

    names = [x["application"] for x in sorted_apps]
    vals = list(range(1, len(sorted_apps)+1))

    colors = ["green", "limegreen", "gold", "orange", "red"]

    ax3.barh(names, vals, color=colors)

    ax3.set_facecolor("#111827")
    fig3.patch.set_facecolor("#111827")

    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')

    for spine in ax3.spines.values():
        spine.set_color("white")

    ax3.set_title("Migration Execution Timeline", color="white")

    st.pyplot(fig3)

# ----------------------------
# Dynamic Recommendations
# ----------------------------
with right2:
    st.subheader("AI Recommendations")

    for rec in recommendations["recommendations"]:
        st.markdown(f"**{rec['application']}**")

        for item in rec["recommendations"][:2]:
            st.markdown(f"<span style='font-size:16px;color:white'>• {item}</span>", unsafe_allow_html=True)
# ----------------------------
# Dynamic AI Narrative
# ----------------------------

sorted_apps = sorted(scores["scores"], key=lambda x: x["score"], reverse=True)

app_lines = []

for app in sorted_apps:
    app_lines.append(
        f"{app['application']} (Risk {app['score']})"
    )

app_summary = ", ".join(app_lines)

granite_output = f"""
Migration priority order based on enterprise risk portfolio:

{app_summary}

Highest-risk applications require early dependency validation, authentication checks, database readiness, and rollback controls.

Migration should begin with lower dependency systems and progressively move toward critical enterprise platforms to reduce blast radius.
"""
# ----------------------------
# Granite Narrative
# ----------------------------
st.subheader("AI Migration Narrative")

clean_output = granite_output.replace("</div>", "").replace("<div>", "").strip()

st.markdown(
    f"""
    <div style='background-color:#0b1f3a;
                padding:20px;
                border-radius:10px;
                color:white;
                font-size:16px;
                line-height:1.8'>
    {clean_output}
    </div>
    """,
    unsafe_allow_html=True
)
# ----------------------------
# Blast Radius Chain
# ----------------------------

st.subheader("Blast Radius Impact Chain")

critical_app = sorted_apps[0]["application"]

critical_rec = next(
    r for r in recommendations["recommendations"]
    if r["application"] == critical_app
)

chain = [critical_app] + critical_rec["dependencies"]

chain_html = ""

for idx, item in enumerate(chain):

    color = "red" if idx == 0 else "#1f77b4"

    chain_html += f"""
    <div style='display:inline-block;
                padding:10px 20px;
                margin:5px;
                background-color:{color};
                color:white;
                border-radius:8px;
                font-weight:bold'>
        {item}
    </div>
    """

st.markdown(chain_html, unsafe_allow_html=True)
# ----------------------------
# Cloud Target Decision
# ----------------------------

st.subheader("Cloud Target Decision")

with open(os.path.join(DATASET_DIR, "migration_decisions.json")) as f:
    decisions = json.load(f)

for item in decisions["decisions"]:
    app = item["application"]
    decision = item["decision"]

    if decision == "HOLD":
        color = "red"
    elif decision == "CONDITIONAL":
        color = "orange"
    else:
        color = "green"

    st.markdown(
        f"""
        <div style='padding:10px;
                    margin:5px;
                    border-radius:8px;
                    background-color:{color};
                    color:white;
                    font-weight:bold'>
            {app} → {decision}
        </div>
        """,
        unsafe_allow_html=True
    )
    # ----------------------------
# Executive Summary Panel
# ----------------------------

st.subheader("Executive Summary")

critical = len([x for x in scores["scores"] if x["score"] >= 90])

medium = len([x for x in scores["scores"] if 70 <= x["score"] < 90])

low = len([x for x in scores["scores"] if x["score"] < 70])

hold = len([x for x in decisions["decisions"] if x["decision"] == "HOLD"])

ready = len([x for x in decisions["decisions"] if x["decision"] == "READY"])

conditional = len([x for x in decisions["decisions"] if x["decision"] == "CONDITIONAL"])

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f"""
        <div style='background:red;padding:20px;border-radius:10px;color:white;text-align:center'>
        Critical Applications<br><h2>{critical}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div style='background:orange;padding:20px;border-radius:10px;color:white;text-align:center'>
        Applications on HOLD<br><h2>{hold}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style='background:green;padding:20px;border-radius:10px;color:white;text-align:center'>
        Ready for Migration<br><h2>{ready}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------
# Live Application Selector
# ----------------------------

st.subheader("Live AI Application Analysis")

app_names = [x["application"] for x in scores["scores"]]

selected_app = st.selectbox(
    "Select application for AI migration reasoning",
    app_names
)

selected_score = next(
    x["score"] for x in scores["scores"]
    if x["application"] == selected_app
)

selected_rec = next(
    r for r in recommendations["recommendations"]
    if r["application"] == selected_app
)

dependencies = ", ".join(selected_rec["dependencies"])

decision = next(
    d["decision"] for d in decisions["decisions"]
    if d["application"] == selected_app
)

prompt = f"""
Explain migration priority for {selected_app}.

Risk score: {selected_score}
Dependencies: {dependencies}
Decision: {decision}

Provide exactly 3 dash bullets using '-' only.
Do not use numbering above 3.
Each bullet must be one short sentence.
"""

ai_response = model.generate_text(prompt=prompt)[:500]

ai_response = ai_response.replace("\n\n", " ")
ai_response = ai_response.replace("\n", " ")
ai_response = ai_response.replace("1.", "<b>1.</b> ")
ai_response = ai_response.replace("2.", "<b>2.</b> ")
ai_response = ai_response.replace("3.", "<b>3.</b> ")
ai_response = ai_response.replace("4.", "")
ai_response = ai_response.replace("5.", "")
ai_response = ai_response.replace("6.", "")
ai_response = ai_response.replace("7.", "")

st.markdown(
    f"""
    <div style='background-color:#071633;
                padding:20px;
                border-radius:10px;
                color:white;
                font-size:16px;
                line-height:1.8'>
    {ai_response}
    </div>
    """,
    unsafe_allow_html=True
)

prompt = f"""
Enterprise migration assessment:

Application: {selected_app}
Risk Score: {selected_score}
Dependencies: {dependencies}
Migration Decision: {decision}

Explain:
1. migration priority
2. dependency criticality
3. blast radius
4. migration wave recommendation
"""

with st.spinner("Granite generating migration reasoning..."):
    live_ai_output = model.generate_text(prompt=prompt)

st.info(live_ai_output)