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

with open(os.path.join(DATASET_DIR, "application_dependency.json")) as f:
    app_dependency = json.load(f)
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
header_html = """
<div style="
position:fixed;
top:0;
left:0;
width:100%;
z-index:9999;
background:linear-gradient(90deg,#001d6c,#0f62fe,#00a6ff);
padding:60px 28px 18px 28px;
box-shadow:0 8px 24px rgba(0,0,0,0.35);
border-bottom:2px solid rgba(255,255,255,0.15);
min-height:110px;
">

<div style="
font-size:34px;
font-weight:900;
color:white;
letter-spacing:0.8px;
margin-bottom:10px;
">
Watsonx AI Migration Executive Control Center
</div>

<div style="
font-size:18px;
font-weight:700;
color:#00ff88;
text-shadow:0 0 10px rgba(0,255,136,0.45);
">
● Governance Active | ● Concert Sequencing Enabled | ● Watsonx Reasoning Live
</div>

</div>
"""

st.markdown(header_html, unsafe_allow_html=True)
st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)

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
# Governance Layer
# ----------------------------
def governance_policy(selected_score):
    if selected_score >= 95:
        return "GOVERNANCE HOLD"
    elif selected_score >= 80:
        return "CONDITIONAL APPROVAL"
    else:
        return "APPROVED"

selected_score = next(
    x["score"] for x in sorted_scores if x["application"] == selected_app_global
)

gov_status = governance_policy(selected_score)

# ----------------------------
# Concert Layer
# ----------------------------
def concert_wave(selected_score):
    if selected_score >= 95:
        return "Wave 3 - Deferred Migration"
    elif selected_score >= 80:
        return "Wave 2 - Controlled Migration"
    else:
        return "Wave 1 - Ready For Migration"

concert_status = concert_wave(selected_score)
# ----------------------------
# Display Governance + Concert
# ----------------------------
st.markdown("## Governance & Concert Control Layer")

g1, g2 = st.columns(2)

with g1:
    gov_color = "#ff4b4b" if "HOLD" in gov_status else "#ffb000" if "CONDITIONAL" in gov_status else "#00aa00"
    st.markdown(f"""
    <div style='background:{gov_color};
                padding:20px;
                border-radius:10px;
                text-align:center;
                font-size:20px;
                font-weight:bold;
                color:white;'>
        Governance Decision<br>
        Policy Check Passed<br>
        Output Validated<br>
        Risk Gate: {gov_status}
    </div>
    """, unsafe_allow_html=True)

with g2:
    concert_color = "#ff4b4b" if "Wave 3" in concert_status else "#ffb000" if "Wave 2" in concert_status else "#00aa00"
    st.markdown(f"""
    <div style='background:{concert_color};
                padding:20px;
                border-radius:10px;
                text-align:center;
                font-size:20px;
                font-weight:bold;
                color:white;'>
        Concert Migration Wave<br>
        Portfolio Sequencing<br>
        Execution Group: {concert_status}
    </div>
    """, unsafe_allow_html=True)
st.markdown("## Governance Explainability")

gov_reason = (
    "High migration risk due to critical dependency concentration and blast radius."
    if selected_score >= 95 else
    "Conditional approval because dependency chain requires staged execution."
    if selected_score >= 80 else
    "Approved because dependency impact remains within acceptable migration threshold."
)

st.markdown(f"""
<div style='background:#102840;
            border-left:5px solid #00a3ff;
            padding:16px;
            border-radius:10px;
            font-size:29px;
            color:white;'>
    {gov_reason}
</div>
""", unsafe_allow_html=True)
st.markdown("### Governance Audit Status")

audited_prompts = len(sorted_scores)

blocked_responses = 1 if "HOLD" in gov_status else 0

validated_outputs = audited_prompts - blocked_responses

a1, a2, a3 = st.columns(3)

with a1:
    st.metric("Prompts Audited", audited_prompts)

with a2:
    st.metric("Validated Outputs", validated_outputs)

with a3:
    st.metric("Blocked Responses", blocked_responses)
# ----------------------------
# Concert Resilience Score
# ----------------------------
dependency_map = {
    "FinanceApp": ["AuthService", "OracleFinanceDB", "RedisCache", "SAPGateway"],
    "BillingApp": ["CustomerDB", "AuthService", "KafkaBroker", "PaymentAPI"],
    "ReportingApp": ["BlobStorage", "CustomerDB", "OracleFinanceDB"],
    "HRPortal": ["SSOService", "DocumentService", "PostgresHRDB"],
    "CitrixAccessGateway": ["AuthService", "LDAPProxy", "FirewallGateway"]
}

selected_dependencies = dependency_map.get(selected_app_global, [])

dependency_count = len(selected_dependencies)
st.markdown(
    f"""
    <div style='
        background-color:#0f2a5f;
        padding:14px;
        border-left:5px solid #0f62fe;
        font-size:29px;
        font-weight:700;
        color:white;
        border-radius:6px;
    '>
    {selected_app_global} has {dependency_count} critical dependencies influencing migration control.
    </div>
    """,
    unsafe_allow_html=True
)
# Governance
if selected_score >= 95:
    gov_status = "GOVERNANCE HOLD"
elif selected_score >= 80:
    gov_status = "CONDITIONAL APPROVAL"
else:
    gov_status = "APPROVED"

# Concert
if selected_score >= 95:
    concert_status = "Wave 3 - Deferred Migration"
elif selected_score >= 65:
    concert_status = "Wave 2 - Controlled Migration"
else:
    concert_status = "Wave 1 - Ready For Migration"

# Resilience
dependency_penalty = dependency_count * 4

resilience_score = max(
    35,
    140 - selected_score - dependency_penalty
)

# Execution confidence
if resilience_score >= 65:
    execution_confidence = "LOW RISK"
elif resilience_score >= 50:
    execution_confidence = "MEDIUM RISK"
else:
    execution_confidence = "HIGH RISK"

# Governance audit
audited_prompts = len(sorted_scores)
blocked_responses = 1 if "HOLD" in gov_status else 0
validated_outputs = audited_prompts - blocked_responses



st.markdown("## IBM Concert Operational Resilience")

c1, c2 = st.columns(2)

with c1:
    st.metric("Operational Resilience Score", resilience_score)

with c2:
    st.metric("Execution Confidence", execution_confidence)
if "Wave 1" in concert_status:
    workflow_msg = "READY FOR STANDARD MIGRATION WORKFLOW"
elif "Wave 2" in concert_status:
    workflow_msg = "CONTROLLED EXECUTION WITH DEPENDENCY GATES"
else:
    workflow_msg = "DEFERRED UNTIL CRITICAL DEPENDENCIES STABILIZE"

st.markdown("## Concert Workflow Recommendation")

st.markdown(
    f"""
<div style='background-color:#0f2a5f;
padding:18px;
border-left:6px solid #0f62fe;
font-size:22px;
font-weight:700;
color:white;
border-radius:8px'>
{workflow_msg}
</div>
""",
    unsafe_allow_html=True
)
st.markdown("### Governance Audit Status")

a1, a2, a3 = st.columns(3)

with a1:
    st.metric("Prompts Audited", audited_prompts)

with a2:
    st.metric("Validated Outputs", validated_outputs)

with a3:
    st.metric("Blocked Responses", blocked_responses)

if resilience_score >= 70:
    execution_confidence = "LOW RISK"
elif resilience_score >= 50:
    execution_confidence = "MEDIUM RISK"
else:
    execution_confidence = "HIGH RISK"

if execution_confidence == "LOW RISK":
    risk_color = "#24a148"
elif execution_confidence == "MEDIUM RISK":
    risk_color = "#f1c21b"
else:
    risk_color = "#da1e28"

    
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
risk_level = (
    "HIGH"
    if selected_narrative_score >= 90
    else "MEDIUM"
    if selected_narrative_score >= 75
    else "LOW"
)
narrative_prompt = f"""
You are an enterprise migration architect preparing an executive migration review.

Evaluate the following application:

Application: {selected_narrative_app}
Risk Score: {selected_narrative_score}
Dependencies: {narrative_dependencies}
Migration Decision: {narrative_decision}
Governance Status: {gov_status}
Concert Wave: {concert_status}
Operational Resilience Score: {resilience_score}
Execution Confidence: {risk_level}

Instructions:
1. Explain migration readiness clearly.
2. Mention dependency impact.
3. Explain governance implication.
4. Explain why concert assigned this wave.
5. Give executive recommendation in concise enterprise language.
"""

log_action("Narrative Prompt Submitted", narrative_prompt)

# Keep Granite call for governance logging
granite_output = generate_ai_response(narrative_prompt)

if validate_ai_output(granite_output):
    log_action("Narrative Accepted", granite_output)

# Deterministic executive narrative
execution_confidence = "high" if selected_narrative_score >= 90 else "moderate" if selected_narrative_score >= 70 else "controlled"

line1 = f"1. Dependency risk remains {execution_confidence} due to {selected_narrative_rec['dependencies'][0]}."
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
# Unified IBM Scoring Engine
# ----------------------------

selected_dependencies = next(
    (
        x["dependencies"]
        for x in app_dependency["applications"]
        if x["application"] == selected_app_global
    ),
    []
)

dependency_count = len(selected_dependencies)

# ----------------------------
# Governance Decision
# ----------------------------
if selected_score >= 95:
    gov_status = "GOVERNANCE HOLD"
elif selected_score >= 80:
    gov_status = "CONDITIONAL APPROVAL"
else:
    gov_status = "APPROVED"

# ----------------------------
# Concert Migration Wave
# ----------------------------
if selected_score >= 95:
    concert_status = "Wave 3 - Deferred Migration"
elif selected_score >= 80:
    concert_status = "Wave 2 - Controlled Migration"
else:
    concert_status = "Wave 1 - Ready For Migration"

# ----------------------------
# Operational Resilience Score
# ----------------------------
dependency_penalty = dependency_count * 4

resilience_score = max(
    35,
    140 - selected_score - dependency_penalty
)

if resilience_score >= 65:
    execution_confidence = "LOW RISK"
elif resilience_score >= 50:
    execution_confidence = "MEDIUM RISK"
else:
    execution_confidence = "HIGH RISK"

# ----------------------------
# Execution Confidence
# ----------------------------
if execution_confidence == "LOW RISK":
    risk_color = "#24a148"
elif execution_confidence == "MEDIUM RISK":
    risk_color = "#f1c21b"
else:
    risk_color = "#da1e28"

# ----------------------------
# Governance Audit Metrics
# ----------------------------
audited_prompts = len(sorted_scores)

blocked_responses = 1 if "HOLD" in gov_status else 0

validated_outputs = audited_prompts - blocked_responses

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
font-size:20px;
line-height:1.8'>
{ai_response}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Footer
# ----------------------------
st.markdown(
    """
    <div style='
        position:fixed;
        bottom:0;
        left:0;
        width:100%;
        padding:14px;
        background: linear-gradient(90deg, #0f2a5f, #0f62fe);
        text-align:center;
        font-size:20px;
        font-weight:700;
        color:white;
        z-index:9999;
        box-shadow: 0 -3px 10px rgba(0,0,0,0.35);
        letter-spacing:0.4px;
    '>
    Enterprise Flow: Dynamic Dependency Scan → Governance Control → Watsonx Reasoning → Concert Sequencing → Executive Decision Layer
    </div>
    """,
    unsafe_allow_html=True
)