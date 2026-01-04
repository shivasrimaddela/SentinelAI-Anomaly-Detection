from flask import Blueprint, jsonify
from pathlib import Path
import json
from src.config import LOG_PATH, ALERT_LOG_PATH

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['GET'])
def get_logs():
    logs = []

    # 1️⃣ Read normal logs
    if Path(LOG_PATH).exists():
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f.readlines()[-50:]:
                logs.append({
                    "raw": line.strip(),
                    "type": "normal"
                })

    # 2️⃣ Read alert logs
    if Path(ALERT_LOG_PATH).exists():
        with open(ALERT_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f.readlines()[-20:]:
                try:
                    alert = json.loads(line.strip())
                    logs.append({
                        "raw": alert["log"],
                        "type": "anomaly",
                        "severity": alert.get("severity", "HIGH")
                    })
                except json.JSONDecodeError:
                    pass

    # 3️⃣ Sort latest first
    logs = logs[::-1]

    return jsonify({
        "logs": logs,
        "count": len(logs)
    })
