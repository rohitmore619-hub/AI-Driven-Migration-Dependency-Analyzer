import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

with open(os.path.join(DATASET_DIR, "risk_scores.json")) as f:
    risk_scores = json.load(f)

decisions = []

for app in risk_scores["scores"]:

    score = app["score"]

    if score >= 100:
        decision = "HOLD"
    elif score >= 70:
        decision = "CONDITIONAL"
    else:
        decision = "READY"

    decisions.append({
        "application": app["application"],
        "decision": decision
    })

with open(os.path.join(DATASET_DIR, "migration_decisions.json"), "w") as f:
    json.dump({"decisions": decisions}, f, indent=4)

print("migration_decisions.json generated successfully.")