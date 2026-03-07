import json
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

with open(os.path.join(DATASET_DIR, "risk_scores.json")) as f:
    scores = json.load(f)

with open(os.path.join(DATASET_DIR, "migration_decisions.json")) as f:
    decisions = json.load(f)

with open(os.path.join(DATASET_DIR, "recommendations.json")) as f:
    recommendations = json.load(f)

fig = plt.figure(figsize=(16, 9))
fig.patch.set_facecolor("#f2f2f2")

plt.figtext(0.5, 0.94, "AI-Driven Migration Dependency", ha="center", fontsize=28, fontweight="bold")
plt.figtext(0.5, 0.88, "Enterprise Dependency, Risk, and Migration Decision Dashboard", ha="center", fontsize=16)

ax1 = plt.axes([0.08, 0.62, 0.84, 0.12])
ax1.axis("off")

table_data = []

for score in scores["scores"]:

    app = score["application"]
    score_value = score["score"]

    decision = next(d["decision"] for d in decisions["decisions"] if d["application"] == app)

    dep_count = next(len(r["dependencies"]) for r in recommendations["recommendations"] if r["application"] == app)

    if score_value >= 100:
        level = "Critical"
    elif score_value >= 70:
        level = "Medium"
    else:
        level = "Low"

    table_data.append([app, score_value, level, dep_count, decision])

table = ax1.table(
    cellText=table_data,
    colLabels=["Application", "Risk Score", "Risk Level", "Dependency Count", "Migration Decision"],
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 1.3)

for i, row in enumerate(table_data):

    score = row[1]

    if score >= 100:
        table[(i+1,1)].set_facecolor("red")
    elif score >= 70:
        table[(i+1,1)].set_facecolor("orange")
    else:
        table[(i+1,1)].set_facecolor("green")

# Dependency Graph
plt.figtext(0.08, 0.48, "Dependency Graph", fontsize=10, fontweight="bold")

y = 0.43
for rec in recommendations["recommendations"]:
    line = rec["application"] + " → " + " → ".join(rec["dependencies"])
    plt.figtext(0.08, y, line, fontsize=7)
    y -= 0.035

# Critical Path
plt.figtext(0.52, 0.43, "Critical Path", fontsize=10, fontweight="bold")

critical_apps = sorted(scores["scores"], key=lambda x: x["score"], reverse=True)[:2]

y = 0.37
for item in critical_apps:
    plt.figtext(0.50, y, f'{item["application"]} = Critical migration path', fontsize=10)
    y -= 0.035

# Migration Waves
plt.figtext(0.75, 0.48, "Migration Waves", fontsize=10, fontweight="bold")

sorted_apps = sorted(scores["scores"], key=lambda x: x["score"])

y = 0.43
for i, item in enumerate(sorted_apps):
    plt.figtext(0.75, y, f'Wave {i+1} → {item["application"]}', fontsize=9)
    y -= 0.035

# Dynamic Recommendations
plt.figtext(0.08, 0.25, "Dynamic Recommendations", fontsize=10, fontweight="bold")

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

    plt.figtext(x, y, f'{rec["application"]}:', fontsize=8)
    y -= 0.025

    for item in rec["recommendations"][:2]:
        plt.figtext(x + 0.02, y, f'• {item}', fontsize=8)
        y -= 0.020

    if idx < 2:
        left_y = y - 0.015
    else:
        right_y = y - 0.015
# AI Migration Narrative (Granite-driven)

with open(os.path.join(DATASET_DIR, "granite_summary.json")) as f:
    granite = json.load(f)

summary_text = granite["summary"]

plt.figtext(0.52, 0.08, "AI Migration Narrative", fontsize=10, fontweight="bold")

plt.figtext(
    0.52,
    0.04,
    summary_text,
    fontsize=8,
    color="black",
    wrap=True
)

plt.axis("off")
plt.show()
