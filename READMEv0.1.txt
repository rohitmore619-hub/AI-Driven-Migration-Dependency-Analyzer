# AI Migration Intelligence Engine  
## Team Understanding Guide

---

# 1. What this tool actually does

AI Migration Intelligence Engine is a migration analysis tool that converts enterprise migration inputs into migration decisions.

Instead of manually reading CMDB, dependency sheets, and code findings separately, the tool combines all technical signals and generates:

- migration risk score
- dependency impact
- blast radius
- migration decision
- recommendations
- dashboard visualization

---

# 2. Why we built this

In real migration projects, teams often face:

- hidden database dependency
- shared authentication services
- undocumented firewall paths
- hardcoded source code references
- legacy runtime compatibility

These are usually discovered late during migration execution.

This tool helps identify them before execution.

---

# 3. What problem it solves

Without this tool:

CMDB + source code + infra + dependency are reviewed separately.

This causes:

- manual effort
- delayed migration decisions
- wrong migration sequencing
- rollback risk

This tool creates one migration decision layer.

---

# 4. End-to-end architecture flow

Input datasets  
↓  
Dependency Builder  
↓  
Blast Radius Score Engine  
↓  
Decision Engine  
↓  
Recommendation Engine  
↓  
Dashboard / Report

---

# 5. Folder structure

AI_Analyzer_Migration_PoC/

scripts/
- dependency_builder.py
- blast_radius_score.py
- decision_engine.py
- recommendation_engine.py
- code_analysis_engine.py
- sca_engine.py
- report_generator.py

datasets/
- application_dependency.json
- database_dependency.json
- authentication_dependency.json
- runtime_dependency.json
- source_code_risk.json
- network_security.json
- legacy_compatibility_risk.json
- infra_inventory.json
- cmdb_assets.json
- recommendations.json

notebooks/
- AI_Migration_Master_Notebook.ipynb

reports/
- enterprise_migration_report.pdf

---

# 6. Script purpose

## dependency_builder.py

Reads all dependency datasets and creates consolidated dependency_output.json

Purpose:
Builds application relationship model.

---

## blast_radius_score.py

Calculates technical impact score.

Uses weighted scoring:

- Database dependency = 40
- Authentication dependency = 30
- Legacy runtime = 25
- Source code issue = 25
- Network issue = 20

---

## decision_engine.py

Converts score into migration status.

Rules:

- score >= 100 → HOLD
- score >= 70 → CONDITIONAL
- score < 70 → READY

---

## recommendation_engine.py

Generates remediation based on detected blockers.

Example:

Database issue → validate DB path  
Authentication issue → validate identity integration

---

## code_analysis_engine.py

Scans source files dynamically.

Detects:

- hardcoded secrets
- static tokens
- risky strings

---

## sca_engine.py

Reads dependency package findings.

Detects:

- vulnerable packages
- version exposure

---

## report_generator.py

Builds executive PDF report.

---

# 7. Local execution sequence

Run exactly in this order:

python dependency_builder.py  
python blast_radius_score.py  
python decision_engine.py  
python recommendation_engine.py  
python code_analysis_engine.py  
python sca_engine.py  
python report_generator.py  

---

# 8. Output generated after each step

## dependency_builder.py

Output:

dependency_output.json

---

## blast_radius_score.py

Output:

risk_scores.json

---

## decision_engine.py

Output:

migration_decisions.json

---

## recommendation_engine.py

Output:

recommendations.json

---

## report_generator.py

Output:

enterprise_migration_report.pdf

---

# 9. Dashboard output

Notebook dashboard shows:

- Migration Risk Portfolio
- Dependency Criticality
- CMDB Asset Intelligence
- Blast Radius Chain
- Architecture Path
- Cloud Target
- Migration Timeline
- AI Narrative

---

# 10. Which parts are dynamic

Dynamic from JSON:

- risk scores
- dependency chain
- CMDB values
- recommendations

Changing JSON changes dashboard automatically.

---

# 11. Which parts are still demo placeholders

Still fixed demo logic:

- AI confidence %
- target cloud labels
- migration timeline order

These can later move into:

- decision_engine.py
- cloud_target.json
- migration_wave.json

---

# 12. If we move to IBM watsonx

No major logic change required.

Notebook runs directly.

Possible future upgrade:

- watsonx AI for narrative generation
- watsonx data for CMDB lake
- watsonx governance for explainability

---

# 13. What colleagues should remember

This tool does NOT replace:

- CMDB
- SonarQube
- Azure Migrate
- AWS Migration Hub

It sits above them and converts findings into migration decision logic.

---

# 14. Real enterprise use cases

- on-prem to cloud migration
- VMware to AVS migration
- database modernization
- app modernization

---

# 15. Future enhancement

Possible next step:

- live GitHub repo scan
- Terraform integration
- HCX dependency feed
- API version