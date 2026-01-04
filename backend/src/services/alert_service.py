from datetime import datetime
from pathlib import Path
import json

class AlertService:
    def __init__(self, alert_log_path):
        self.alert_log_path = Path(alert_log_path)
        self.alert_log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_alert(self, log_line, severity="HIGH", metadata=None):
        alert_entry = {
            "timestamp": datetime.now().isoformat(),
            "log": log_line,
            "severity": severity,
            "metadata": metadata or {}
        }
        with open(self.alert_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(alert_entry) + "\n")

    def get_recent_alerts(self, limit=50):
        if not self.alert_log_path.exists():
            return []

        with open(self.alert_log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        alerts = []
        for line in lines[-limit:]:
            try:
                alerts.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                alerts.append({
                    "log": line.strip(),
                    "timestamp": None,
                    "severity": "UNKNOWN",
                    "metadata": {}
                })
        return alerts

    def get_alert_count(self):
        if not self.alert_log_path.exists():
            return 0
        with open(self.alert_log_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
