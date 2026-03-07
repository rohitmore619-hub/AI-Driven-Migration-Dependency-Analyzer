import json

with open("../datasets/sca_findings.json") as f:
    sca = json.load(f)

results = []

for comp in sca["components"]:
    severity_score = (
        comp["critical"] * 40 +
        comp["high"] * 25 +
        comp["medium"] * 10 +
        comp["low"] * 5
    )

    results.append({
        "component": comp["component"],
        "score": severity_score,
        "version": comp["version"]
    })

print(json.dumps(results, indent=4))