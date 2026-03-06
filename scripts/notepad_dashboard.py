import json
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

# Load files
with open(os.path.join(DATASET_DIR, "risk_scores.json")) as f:
    scores = json.load(f)

with open(os.path.join(DATASET_DIR, "migration_decisions.json")) as f:
    decisions = json.load(f)

with open(os.path.join(DATASET_DIR, "recommendations.json")) as f:
    recommendations = json.load(f)

# Figure setup
fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor("#f2f2f2")

# Title
plt.figtext(0.5, 0.94, "AI-Driven Migration Dependency", ha="center", fontsize=28)
plt.figtext(0.5, 0.88, "Enterprise Dependency, Risk, and Migration Decision Dashboard", ha="center", fontsize=16)

# ---------------- TABLE ----------------
ax1 = plt.axes([0.08, 0.56, 0.84, 0.14])
ax1.axis("off")

table_data = []

for score in scores["scores"]:

    app = score["application"]
    score_value = score["score"]

    decision = next(
        d["decision"]
        for d in decisions["decisions"]
        if d["application"] == app
    )

    dependency_count = next(
        len(r["dependencies"])
        for r in recommendations["recommendations"]
        if r["application"] == app
    )

    if score_value >= 100:
        level = "Critical"
    elif score_value >= 70:
        level = "Medium"
    else:
        level = "Low"

    table_data.append([
        app,
        score_value,
        level,
        dependency_count,
        decision
    ])

table = ax1.table(
    cellText=table_data,
    colLabels=["Application", "Risk Score", "Risk Level", "Dependency Count", "Migration Decision"],
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.3)

# Risk colors
for i, row in enumerate(table_data):

    score = row[1]

    if score >= 100:
        table[(i+1,1)].set_facecolor("red")
    elif score >= 70:
        table[(i+1,1)].set_facecolor("orange")
    else:
        table[(i+1,1)].set_facecolor("green")

# ---------------- DEPENDENCY GRAPH ----------------
plt.figtext(0.08, 0.48, "Dependency Graph", fontsize=18, fontweight="bold")

graph_text = [
    "FinanceApp → OracleFinanceDB → AuthService",
    "BillingApp → CustomerDB → AuthService",
    "ReportingApp → OracleFinanceDB",
    "CitrixAccessGateway → AuthService"
]

y = 0.43
for line in graph_text:
    plt.figtext(0.08, y, line, fontsize=11)
    y -= 0.035

# ---------------- CRITICAL PATH ----------------
plt.figtext(0.50, 0.48, "Critical Path", fontsize=18, fontweight="bold")

critical = [
    "FinanceApp = Migration blocker",
    "OracleFinanceDB = Shared critical DB"
]

y = 0.43
for line in critical:
    plt.figtext(0.50, y, line, fontsize=11)
    y -= 0.035

# ---------------- MIGRATION WAVES ----------------
plt.figtext(0.75, 0.48, "Migration Waves", fontsize=18, fontweight="bold")

waves = [
    "Wave 1 → CitrixAccessGateway",
    "Wave 2 → ReportingApp",
    "Wave 3 → BillingApp",
    "Wave 4 → FinanceApp"
]

y = 0.43
for line in waves:
    plt.figtext(0.75, y, line, fontsize=11)
    y -= 0.035

# ---------------- DYNAMIC RECOMMENDATIONS ----------------
plt.figtext(0.08, 0.25, "Dynamic Recommendations", fontsize=18, fontweight="bold")

left_x = 0.08
right_x = 0.50

left_y = 0.20
right_y = 0.20

for idx, rec in enumerate(recommendations["recommendations"]):

    if idx < 2:
        x = left_x
        y = left_y
    else:
        x = right_x
        y = right_y

    plt.figtext(x, y, f'{rec["application"]}:', fontsize=11)
    y -= 0.025

    for item in rec["recommendations"][:2]:
        plt.figtext(x + 0.02, y, f'• {item}', fontsize=10)
        y -= 0.022

    if idx < 2:
        left_y = y - 0.02
    else:
        right_y = y - 0.02

# Final render
plt.axis("off")
plt.show()