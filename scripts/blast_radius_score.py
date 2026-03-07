import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

def load_json(filename):
    with open(os.path.join(DATASET_DIR, filename)) as f:
        return json.load(f)

app_dep = load_json("application_dependency.json")
db_dep = load_json("database_dependency.json")
auth_dep = load_json("authentication_dependency.json")
runtime_dep = load_json("runtime_dependency.json")
code_dep = load_json("source_code_risk.json")
weights = load_json("risk_weight_config.json")

scores = []

for app in app_dep["applications"]:

    app_name = app["application"]
    score = 0

    dependencies = app.get("dependencies", [])

    score += len(dependencies) * weights["dependency_weight"]

    for db in db_dep["database_dependencies"]:
        if db["application"] == app_name:
            score += weights["database_weight"]

    for auth in auth_dep["authentication_dependencies"]:
        if auth["application"] == app_name:
            score += weights["authentication_weight"]

    for runtime in runtime_dep["runtime_dependencies"]:
        if runtime["application"] == app_name:
            score += weights["runtime_weight"]

    for code in code_dep["source_code_risks"]:
        if code["application"] == app_name:
            score += weights["source_code_weight"]

    scores.append({
        "application": app_name,
        "score": score
    })

with open(os.path.join(DATASET_DIR, "risk_scores.json"), "w") as f:
    json.dump({"scores": scores}, f, indent=4)

print("risk_scores.json generated successfully.")