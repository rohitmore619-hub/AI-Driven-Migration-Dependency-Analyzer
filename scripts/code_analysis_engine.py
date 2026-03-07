import json

with open("../datasets/source_code_findings.json") as f:
    findings = json.load(f)

results = []

for app in findings["applications"]:
    total_score = 0

    for finding in app["findings"]:
        total_score += finding["cvss"]

    results.append({
        "application": app["application"],
        "total_code_score": total_score,
        "findings": app["findings"]
    })

print(json.dumps(results, indent=4))