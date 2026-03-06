Local Execution Guide

1. Folder Structure
AI_Analyzer_Migration_PoC/
 ├── scripts/
 │    ├── dependency_builder.py
 │    ├── blast_radius_score.py
 │    ├── decision_engine.py
 │    ├── recommendation_engine.py
 │    ├── notepad_dashboard.py
 │
 ├── datasets/
 │    ├── application_dependency.json
 │    ├── database_dependency.json
 │    ├── authentication_dependency.json
 │    ├── runtime_dependency.json
 │    ├── source_code_risk.json
 │    ├── network_security.json
 │    ├── legacy_compatibility_risk.json
 │    ├── infra_inventory.json
 │
 ├── outputs (auto-generated)
 │    ├── dependency_output.json
 │    ├── risk_scores.json
 │    ├── migration_decisions.json
 │    ├── recommendations.json

2. Execution Order

Step 1:
python dependency_builder.py
Expected Output: dependency_output.json

Step 2:
python blast_radius_score.py
Expected Output: risk_scores.json

Step 3:
python decision_engine.py
Expected Output: migration_decisions.json

Step 4:
python recommendation_engine.py
Expected Output: recommendations.json

Step 5:
python notepad_dashboard.py
Expected Output: visual dashboard window

3. Parameters Used

dependency_builder.py
- Reads all dependency JSON files dynamically
- Builds consolidated application dependency model

blast_radius_score.py
- Calculates risk score using dependency count + technical risk

decision_engine.py
- Applies thresholds:
  score >= 100 => HOLD
  score >= 70 => CONDITIONAL
  score < 70 => READY

recommendation_engine.py
- Generates recommendations dynamically from dependency type

notepad_dashboard.py
- Renders dashboard using generated outputs

4. Input Dataset Rules

Each JSON must contain:
- application name
- dependency values
- risk indicators

Example:
{ "application": "FinanceApp", "database": "OracleFinanceDB" }

5. Troubleshooting

If FileNotFoundError occurs:
- Check scripts folder and datasets folder are under same parent directory

If KeyError occurs:
- Verify JSON key names match expected schema

If dashboard empty:
- Ensure all previous scripts executed successfully

6. Expected Final Result

- Risk score generated
- Migration decision generated
- Dynamic recommendations shown
- Dependency graph shown
- Critical path shown
- Migration wave suggestion shown
