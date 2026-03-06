import json
import os

# Base path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

# Files
app_file = os.path.join(DATASET_DIR, "application_dependency.json")
db_file = os.path.join(DATASET_DIR, "database_dependency.json")
auth_file = os.path.join(DATASET_DIR, "authentication_dependency.json")
runtime_file = os.path.join(DATASET_DIR, "runtime_dependency.json")
source_file = os.path.join(DATASET_DIR, "source_code_risk.json")
network_file = os.path.join(DATASET_DIR, "network_security.json")
legacy_file = os.path.join(DATASET_DIR, "legacy_compatibility_risk.json")

risk_file = os.path.join(DATASET_DIR, "risk_scores.json")

# Load JSONs
with open(app_file) as f:
    app_data = json.load(f)

with open(db_file) as f:
    db_data = json.load(f)

with open(auth_file) as f:
    auth_data = json.load(f)

with open(runtime_file) as f:
    runtime_data = json.load(f)

with open(source_file) as f:
    source_data = json.load(f)

with open(network_file) as f:
    network_data = json.load(f)

with open(legacy_file) as f:
    legacy_data = json.load(f)

# Dynamic key resolver
def get_app_name(item):
    return item.get("application") or item.get("app") or item.get("name") or item.get("service")

scores_output = []

for app in app_data["applications"]:

    app_name = get_app_name(app)
    score = 0

    # 1. Application dependencies
    score += len(app.get("depends_on", [])) * 20

    # 2. Database dependency
    for db in db_data.get("databases", []):
        if get_app_name(db) == app_name:
            score += 25

    # 3. Authentication dependency
    for auth in auth_data.get("authentication", []):
        if get_app_name(auth) == app_name:
            score += 20

    # 4. Runtime dependency
    for runtime in runtime_data.get("runtime", []):
        if get_app_name(runtime) == app_name:
            score += 20

    # 5. Source code risk
    for src in source_data.get("source_code", []):
        if get_app_name(src) == app_name:
            score += 15

    # 6. Network security dependency
    for net in network_data.get("network", []):
        if get_app_name(net) == app_name:
            score += 15

    # 7. Legacy risk
    for legacy in legacy_data.get("legacy", []):
        if get_app_name(legacy) == app_name:
            score += 20

    scores_output.append({
        "application": app_name,
        "score": score
    })

# Save output
with open(risk_file, "w") as f:
    json.dump({"scores": scores_output}, f, indent=4)

print("\nrisk_scores.json generated successfully.")