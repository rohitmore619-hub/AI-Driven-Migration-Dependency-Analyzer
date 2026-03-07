import os
import json
from datetime import datetime

import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image
)

from reportlab.graphics.shapes import Drawing, Rect, String, Line


# ============================================================
# PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = os.path.join(BASE_DIR, f"enterprise_migration_report_{timestamp}.pdf")


# ============================================================
# SAFE JSON LOADER
# ============================================================
def load_json(filename):
    path = os.path.join(DATASET_DIR, filename)

    if not os.path.exists(path):
        return []

    if os.path.getsize(path) == 0:
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# LOAD DATASETS
# ============================================================
risk_scores = load_json("risk_scores.json")
migration_decisions = load_json("migration_decisions.json")
recommendations = load_json("recommendations.json")
sca_findings = load_json("sca_findings.json")
cmdb_assets = load_json("cmdb_assets.json")
dependency_output = load_json("dependency_output.json")


scores = risk_scores.get("scores", []) if isinstance(risk_scores, dict) else risk_scores
decisions = migration_decisions.get("decisions", []) if isinstance(migration_decisions, dict) else migration_decisions
recs = recommendations.get("recommendations", []) if isinstance(recommendations, dict) else recommendations
sca = sca_findings if isinstance(sca_findings, list) else sca_findings.get("findings", [])
assets = cmdb_assets if isinstance(cmdb_assets, list) else cmdb_assets.get("assets", [])
deps = dependency_output.get("dependencies", []) if isinstance(dependency_output, dict) else dependency_output


# ============================================================
# GRAPH 1 — RISK BAR CHART
# ============================================================
apps = [x.get("application", "NA") for x in scores]
values = [x.get("score", 0) for x in scores]

plt.figure(figsize=(6, 3))
plt.bar(apps, values)
plt.title("Migration Risk Score")
plt.tight_layout()

risk_chart = os.path.join(BASE_DIR, "risk_chart.png")
plt.savefig(risk_chart)
plt.close()


# ============================================================
# GRAPH 2 — HEATMAP
# ============================================================
heat_values = [[x.get("score", 0)] for x in scores]

plt.figure(figsize=(3, 3))
plt.imshow(heat_values, aspect='auto')
plt.yticks(range(len(apps)), apps)
plt.xticks([])
plt.title("Executive Heatmap")

heatmap_chart = os.path.join(BASE_DIR, "heatmap_chart.png")
plt.tight_layout()
plt.savefig(heatmap_chart)
plt.close()


# ============================================================
# GRAPH 3 — READINESS GAUGE
# ============================================================
avg_score = sum(values) / len(values) if values else 0
readiness = max(0, 100 - avg_score)

plt.figure(figsize=(4, 2))
plt.bar(["Readiness"], [readiness])
plt.ylim(0, 100)
plt.title(f"Migration Readiness = {int(readiness)}%")

gauge_chart = os.path.join(BASE_DIR, "gauge_chart.png")
plt.tight_layout()
plt.savefig(gauge_chart)
plt.close()


# ============================================================
# PDF SETUP
# ============================================================
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()
elements = []


# ============================================================
# COVER PAGE
# ============================================================
elements.append(Paragraph("<b>AI Migration Dependency Analyzer</b>", styles["Title"]))
elements.append(Spacer(1, 20))
elements.append(Paragraph("Enterprise Migration Intelligence Report", styles["Heading2"]))
elements.append(Spacer(1, 20))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%d-%b-%Y')}", styles["BodyText"]))
elements.append(PageBreak())


# ============================================================
# TABLE OF CONTENTS
# ============================================================
elements.append(Paragraph("<b>Table of Contents</b>", styles["Heading2"]))

toc = [
    "1 Executive Summary",
    "2 Risk Visualization",
    "3 Migration Decisions",
    "4 Recommendations",
    "5 Security Findings",
    "6 CVSS Severity",
    "7 CWE Mapping",
    "8 CMDB Assets",
    "9 Blast Radius",
    "10 Architecture View"
]

for item in toc:
    elements.append(Paragraph(item, styles["BodyText"]))

elements.append(PageBreak())


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================
elements.append(Paragraph("<b>1 Executive Summary</b>", styles["Heading2"]))
elements.append(Paragraph(
    "This analyzer correlates infrastructure, CMDB, source code risk, software composition analysis, and dependency blast radius into migration decisions.",
    styles["BodyText"]
))

elements.append(Spacer(1, 20))


# ============================================================
# RISK VISUALS
# ============================================================
elements.append(Paragraph("<b>2 Risk Visualization</b>", styles["Heading2"]))
elements.append(Image(risk_chart, width=400, height=200))
elements.append(Image(heatmap_chart, width=250, height=180))
elements.append(Image(gauge_chart, width=250, height=120))
elements.append(Spacer(1, 20))


# ============================================================
# DECISIONS
# ============================================================
elements.append(Paragraph("<b>3 Migration Decisions</b>", styles["Heading2"]))

for d in decisions:
    elements.append(Paragraph(
        f"{d.get('application')} → {d.get('decision')}",
        styles["BodyText"]
    ))

elements.append(Spacer(1, 20))


# ============================================================
# RECOMMENDATIONS
# ============================================================
elements.append(Paragraph("<b>4 Recommendations</b>", styles["Heading2"]))

for r in recs:
    elements.append(Paragraph(f"<b>{r.get('application')}</b>", styles["BodyText"]))

    for item in r.get("recommendations", []):
        elements.append(Paragraph(f"• {item}", styles["BodyText"]))

elements.append(PageBreak())


# ============================================================
# SECURITY FINDINGS
# ============================================================
elements.append(Paragraph("<b>5 Security Findings</b>", styles["Heading2"]))

sca_table = [["Component", "Version", "Score"]]

for s in sca:
    sca_table.append([
        s.get("component"),
        s.get("version"),
        str(s.get("score"))
    ])

sca_obj = Table(sca_table)
sca_obj.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.purple),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(sca_obj)
elements.append(Spacer(1, 20))


# ============================================================
# CVSS SEVERITY
# ============================================================
elements.append(Paragraph("<b>6 CVSS Severity</b>", styles["Heading2"]))

severity_table = [["Component", "CVSS", "Severity"]]

for item in sca:
    score = item.get("score", 0)

    if score >= 80:
        severity = "Critical"
    elif score >= 60:
        severity = "High"
    elif score >= 40:
        severity = "Medium"
    else:
        severity = "Low"

    severity_table.append([item.get("component"), str(score), severity])

sev_obj = Table(severity_table)
sev_obj.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.purple),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(sev_obj)
elements.append(Spacer(1, 20))


# ============================================================
# CWE MAPPING
# ============================================================
elements.append(Paragraph("<b>7 CWE Mapping</b>", styles["Heading2"]))

cwe_table = [["Component", "CWE"]]

for item in sca:
    score = item.get("score", 0)

    if score >= 80:
        cwe = "CWE-79"
    elif score >= 60:
        cwe = "CWE-89"
    else:
        cwe = "CWE-327"

    cwe_table.append([item.get("component"), cwe])

cwe_obj = Table(cwe_table)
cwe_obj.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.purple),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(cwe_obj)
elements.append(Spacer(1, 20))


# ============================================================
# 8 CMDB ASSET SUMMARY
# ============================================================
elements.append(Paragraph("<b>8 CMDB Asset Summary</b>", styles["Heading2"]))
elements.append(Spacer(1, 10))

cmdb_table = [["Server", "Environment"]]

for a in assets:
    cmdb_table.append([
        a.get("server", "NA"),
        a.get("environment", a.get("env", "NA"))
    ])

cmdb_obj = Table(cmdb_table)

cmdb_obj.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.purple),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(cmdb_obj)
elements.append(Spacer(1, 20))


# ============================================================
# 9 BLAST RADIUS VIEW (FULLY DYNAMIC FROM JSON)
# ============================================================
elements.append(Paragraph("<b>9 Blast Radius View</b>", styles["Heading2"]))
elements.append(Spacer(1, 10))

blast = Drawing(520, 140)

start_y = 110

for dep in deps:
    app = dep.get("application", "NA")
    chain = dep.get("dependencies", [])

    nodes = [app] + chain

    x = 20
    y = start_y

    for i, node in enumerate(nodes):

        blast.add(String(x, y, node))

        if i < len(nodes) - 1:
            blast.add(Line(
                x + 60,
                y + 5,
                x + 90,
                y + 5
            ))

        x += 100

    start_y -= 25

elements.append(blast)
elements.append(Spacer(1, 20))



# ============================================================
# 10 ARCHITECTURE VIEW (FULLY CLEAN)
# ============================================================
elements.append(Paragraph("<b>10 Architecture View</b>", styles["Heading2"]))
elements.append(Spacer(1, 10))

arch = Drawing(520, 150)

layers = [
    ("Applications", 20),
    ("Services", 150),
    ("Databases", 280),
    ("Infrastructure", 410)
]

for label, xpos in layers:
    arch.add(Rect(
        xpos,
        80,
        100,
        40,
        strokeColor=colors.black,
        fillColor=None
    ))

    arch.add(String(
        xpos + 15,
        95,
        label
    ))

for i in range(len(layers) - 1):
    x1 = layers[i][1] + 100
    x2 = layers[i + 1][1]

    arch.add(Line(
        x1,
        100,
        x2,
        100
    ))

elements.append(arch)
elements.append(Spacer(1, 20))


# ============================================================
# BUILD
# ============================================================
doc.build(elements)

print(f"PDF generated successfully: {OUTPUT_FILE}")