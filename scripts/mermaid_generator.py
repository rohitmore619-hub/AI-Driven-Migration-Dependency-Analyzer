import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")

with open(os.path.join(DATASET_DIR, "recommendations.json")) as f:
    data = json.load(f)

mermaid = "flowchart TB\n"

for app in data["recommendations"]:
    source = app["application"]

    for dep in app["dependencies"]:
        mermaid += f"{source} --> {dep}\n"

with open(os.path.join(DATASET_DIR, "mermaid_output.txt"), "w") as f:
    f.write(mermaid)

print("Mermaid generated successfully")