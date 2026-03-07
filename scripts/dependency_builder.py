import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

def load_json(filename):
    with open(os.path.join(DATASET_DIR, filename)) as f:
        return json.load(f)

infra = load_json("infra_inventory.json")
app_dep = load_json("application_dependency.json")

output = []

for app in app_dep["applications"]:
    output.append(app)

with open(os.path.join(DATASET_DIR, "dependency_output.json"), "w") as f:
    json.dump({"dependencies": output}, f, indent=4)

print("dependency_output.json generated successfully.")