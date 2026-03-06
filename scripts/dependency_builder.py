import json
import networkx as nx
import matplotlib.pyplot as plt

# ---------------------------
# Load datasets
# ---------------------------

with open(r'..\datasets\infra_inventory.json') as f:
    infra = json.load(f)

with open(r'..\datasets\application_dependency.json') as f:
    app_dep = json.load(f)

with open(r'..\datasets\database_dependency.json') as f:
    db_dep = json.load(f)

with open(r'..\datasets\network_security.json') as f:
    network = json.load(f)

with open(r'..\datasets\authentication_dependency.json') as f:
    auth = json.load(f)

with open(r'..\datasets\source_code_risk.json') as f:
    code = json.load(f)

with open(r'..\datasets\runtime_dependency.json') as f:
    runtime = json.load(f)

with open(r'..\datasets\legacy_compatibility_risk.json') as f:
    legacy = json.load(f)

# ---------------------------
# Graph creation
# ---------------------------

G = nx.DiGraph()

# ---------------------------
# Infra nodes
# ---------------------------

for server in infra["servers"]:
    G.add_node(server["hostname"], color="lightblue")
    G.add_edge(server["hostname"], server["application"])

# ---------------------------
# Application dependencies
# ---------------------------

for app in app_dep["applications"]:
    app_name = app["application"]
    G.add_node(app_name, color="orange")

    for dep in app["depends_on"]:
        G.add_node(dep, color="yellow")
        G.add_edge(app_name, dep)

# ---------------------------
# Database dependencies
# ---------------------------

for db in db_dep["databases"]:
    db_name = db["database"]
    G.add_node(db_name, color="green")

    for consumer in db["used_by"]:
        G.add_edge(consumer, db_name)

# ---------------------------
# Network risks
# ---------------------------

for rule in network["network_rules"]:
    if rule["status"] == "Blocked":
        issue = f"FW:{rule['target']}"
        G.add_node(issue, color="red")
        G.add_edge(rule["source"], issue)

# ---------------------------
# Authentication risks
# ---------------------------

for item in auth["authentication"]:
    dep = item["dependency"]
    G.add_node(dep, color="purple")
    G.add_edge(item["application"], dep)

# ---------------------------
# Source code risks
# ---------------------------

for item in code["source_code_findings"]:
    risk = f"Code:{item['application']}"
    G.add_node(risk, color="red")
    G.add_edge(item["application"], risk)

# ---------------------------
# Runtime risks
# ---------------------------

for item in runtime["runtime"]:
    risk = f"Runtime:{item['application']}"
    G.add_node(risk, color="pink")
    G.add_edge(item["application"], risk)

# ---------------------------
# Legacy risks
# ---------------------------

for item in legacy["legacy_systems"]:
    risk = f"Legacy:{item['application']}"
    G.add_node(risk, color="brown")
    G.add_edge(item["application"], risk)

# ---------------------------
# Draw graph
# ---------------------------

colors = [G.nodes[node].get("color", "gray") for node in G.nodes()]

plt.figure(figsize=(18, 12))
pos = nx.spring_layout(G, k=1.8, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=colors,
    node_size=2500,
    font_size=8,
    arrows=True
)

plt.title("AI-Driven Enterprise Migration Dependency & Blast Radius Graph")
plt.show()

# ---------------------------
# Console Output
# ---------------------------

print("\nDependency Relationships:\n")
for edge in G.edges():
    print(f"{edge[0]} --> {edge[1]}")