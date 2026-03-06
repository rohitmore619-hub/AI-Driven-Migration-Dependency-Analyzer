import json
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

risk_file = os.path.join(DATASET_DIR, "risk_scores.json")
decision_file = os.path.join(DATASET_DIR, "migration_decisions.json")

# Load risk scores dynamically
with open(risk_file, "r") as f:
    scores_data = json.load(f)

decisions_output = []

print("\nMigration Decision Engine:\n")

for item in scores_data["scores"]:
    app = item["application"]
    score = item["score"]

    # Dynamic scoring logic
    if score >= 100:
        decision = "HOLD"
    elif score >= 70:
        decision = "CONDITIONAL"
    else:
        decision = "READY"

    print(f"{app}: {decision}")

    decisions_output.append({
        "application": app,
        "decision": decision
    })

# Save output dynamically
with open(decision_file, "w") as f:
    json.dump({"decisions": decisions_output}, f, indent=4)

print("\nmigration_decisions.json generated successfully.")