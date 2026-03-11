import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "datasets", "audit_log.json")

def log_action(stage, details):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "stage": stage,
        "details": details
    }

    logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)