import matplotlib.pyplot as plt

# Data
applications = ["FinanceApp", "BillingApp", "ReportingApp"]
scores = [130, 70, 70]
decisions = [
    "HOLD MIGRATION",
    "CONDITIONAL APPROVAL",
    "CONDITIONAL APPROVAL"
]

# Risk colors
colors = []

for score in scores:
    if score >= 100:
        colors.append("red")
    elif score >= 70:
        colors.append("orange")
    else:
        colors.append("green")

# Create figure
fig, ax = plt.subplots(figsize=(12, 5))

# Remove axes
ax.axis('off')

# Build table content
table_data = []

for i in range(len(applications)):
    table_data.append([
        applications[i],
        scores[i],
        decisions[i]
    ])

# Create table
table = ax.table(
    cellText=table_data,
    colLabels=["Application", "Risk Score", "Migration Decision"],
    loc='center'
)

# Style
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 2)

# Color rows
for i in range(len(applications)):
    table[(i+1, 1)].set_facecolor(colors[i])

# Title
plt.title("AI-Driven Migration Control Tower", fontsize=16)

# Show
plt.show()