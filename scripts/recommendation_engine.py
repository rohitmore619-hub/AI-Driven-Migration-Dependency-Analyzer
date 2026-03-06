import json
import os

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

output_file = os.path.join(DATASET_DIR, "recommendations.json")

# Load files
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

# Helper
def get_app_name(item):
    return item.get("application") or item.get("app") or item.get("name") or item.get("service")

recommendations_output = []

for app in app_data["applications"]:

    app_name = get_app_name(app)
    recommendations = []

    # Dependencies
    dependencies = app.get("depends_on", [])

    # Database rules
    for db in db_data.get("databases", []):
        if get_app_name(db) == app_name:
            recommendations.append(f"Validate DB connectivity for {db.get('database', 'database')}")

    # Authentication rules
    for auth in auth_data.get("authentication", []):
        if get_app_name(auth) == app_name:
            recommendations.append("Validate authentication integration")

    # Runtime rules
    for runtime in runtime_data.get("runtime", []):
        if get_app_name(runtime) == app_name:
            recommendations.append(f"Upgrade runtime from {runtime.get('version', 'legacy runtime')}")

    # Source code rules
    for src in source_data.get("source_code", []):
        if get_app_name(src) == app_name:
            recommendations.append("Review source code hardcoded values")

    # Network rules
    for net in network_data.get("network", []):
        if get_app_name(net) == app_name:
            recommendations.append("Validate firewall and ingress rules")

    # Legacy rules
    for legacy in legacy_data.get("legacy", []):
        if get_app_name(legacy) == app_name:
            recommendations.append("Replace legacy dependent components")

    recommendations_output.append({
        "application": app_name,
        "dependencies": dependencies,
        "recommendations": recommendations
    })

# Save
with open(output_file, "w") as f:
    json.dump({"recommendations": recommendations_output}, f, indent=4)

print("\nrecommendations.json generated successfully.")