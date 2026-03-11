import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "sample_code")

dependencies = []

for root, dirs, files in os.walk(SOURCE_DIR):
    for file in files:
        if file.endswith(".cs") or file.endswith(".py"):

            full_path = os.path.join(root, file)

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            imports = re.findall(r'import\s+(\w+)', content)

            dependencies.append({
                "file": file,
                "dependencies": imports
            })

with open(os.path.join(BASE_DIR, "datasets", "dependency_output.json"), "w") as f:
    json.dump({"dependencies": dependencies}, f, indent=4)