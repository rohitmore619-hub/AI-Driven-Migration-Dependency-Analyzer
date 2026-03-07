import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

with open(os.path.join(DATASET_DIR, "application_dependency.json")) as f:
    app_dep = json.load(f)

recommendations_output = []

for app in app_dep["applications"]:

    app_name = app["application"]
    dependencies = app.get("dependencies", [])

    recommendations = []

    if "AuthService" in dependencies:
        recommendations.append("Validate authentication integration")

    if "OracleFinanceDB" in dependencies or "CustomerDB" in dependencies:
        recommendations.append("Validate database connectivity")

    if "RedisCache" in dependencies:
        recommendations.append("Validate cache failover strategy")

    recommendations.append("Upgrade runtime from legacy runtime")

    recommendations = list(dict.fromkeys(recommendations))

    recommendations_output.append({
        "application": app_name,
        "dependencies": dependencies,
        "recommendations": recommendations
    })

with open(os.path.join(DATASET_DIR, "recommendations.json"), "w") as f:
    json.dump({"recommendations": recommendations_output}, f, indent=4)

print("recommendations.json generated successfully.")