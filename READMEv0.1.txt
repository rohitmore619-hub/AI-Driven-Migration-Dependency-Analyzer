AI Analyzer Migration - Enterprise Grade README v2
1. Solution Overview
AI Analyzer Migration PoC is an enterprise migration intelligence engine that analyzes application dependencies, technical risks, migration blockers, and migration readiness dynamically using structured JSON datasets.
2. Architecture Flow
Input Datasets → Dependency Builder → Blast Radius Score Engine → Decision Engine → Recommendation Engine → Dashboard
Detailed Flow:
• Dependency Builder consolidates all application relationships
• Blast Radius Score computes weighted technical risk
• Decision Engine converts score into migration decision
• Recommendation Engine generates dynamic remediation actions
• Dashboard renders executive migration view
3. Folder Structure
AI_Analyzer_Migration_PoC/
 ├── scripts/
 │    ├── dependency_builder.py
 │    ├── blast_radius_score.py
 │    ├── decision_engine.py
 │    ├── recommendation_engine.py
 │    ├── notepad_dashboard.py
 ├── datasets/
 │    ├── application_dependency.json
 │    ├── database_dependency.json
 │    ├── authentication_dependency.json
 │    ├── runtime_dependency.json
 │    ├── source_code_risk.json
 │    ├── network_security.json
 │    ├── legacy_compatibility_risk.json
 │    ├── infra_inventory.json
4. Local Execution Sequence
Step 1: python dependency_builder.py
Expected Output: dependency_output.json
Step 2: python blast_radius_score.py
Expected Output: risk_scores.json
Step 3: python decision_engine.py
Expected Output: migration_decisions.json
Step 4: python recommendation_engine.py
Expected Output: recommendations.json
Step 5: python notepad_dashboard.py
Expected Output: executive dashboard
5. Risk Scoring Logic
Enterprise weighted scoring:
Database dependency = 40
Authentication dependency = 30
Legacy runtime = 25
Source code issue = 25
Network issue = 20
Formula:
Final Score = Sum of active technical risks
Example:
FinanceApp = 40 + 30 + 25 + 25 = 120
6. Decision Logic
If score >= 100 → HOLD
If score >= 70 → CONDITIONAL
If score < 70 → READY
7. Recommendation Logic
Recommendations generated dynamically based on detected dependency type.
Example:
• Database dependency → Open firewall / validate DB reachability
• Authentication dependency → Validate identity integration
• Runtime issue → Upgrade runtime
• Source code issue → Remove hardcoded values
8. Dashboard Output
Dashboard includes:
• Risk summary table
• Dependency graph
• Critical path
• Migration waves
• Dynamic recommendations
9. Expected Enterprise Usage
• Migration wave planning
• Executive risk review
• Dependency-based migration sequencing
• Application modernization prioritization
10. Troubleshooting
If FileNotFoundError occurs:
Verify scripts and datasets folder under same root.
If KeyError occurs:
Validate JSON schema consistency.
If dashboard blank:
Ensure all previous scripts executed successfully.
