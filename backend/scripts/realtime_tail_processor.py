import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.anomaly_detector import AnomalyDetector
from src.services.alert_service import AlertService
from src.config import LOG_PATH, ALERT_LOG_PATH, MODEL_PATH, VECTORIZER_PATH
from src.utils import format_log_line

detector = AnomalyDetector(MODEL_PATH, VECTORIZER_PATH)
alert_service = AlertService(ALERT_LOG_PATH)

SUSPICIOUS_ACTIONS = {
    "port_scan",
    "bruteforce",
    "sql_injection",
    "xss_attack",
    "data_exfiltration",
    "unauthorized_admin_access"
}

SUSPICIOUS_STATUS = {"401", "403", "404", "500"}

def rule_based_anomaly(log_line: str) -> bool:
    parts = log_line.lower().split(',')
    if len(parts) < 7:
        return False

    status = parts[3]
    action = parts[6]

    if status in SUSPICIOUS_STATUS:
        return True

    if any(a in action for a in SUSPICIOUS_ACTIONS):
        return True

    return False

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def main():
    total = 0
    anomalies = 0

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in follow(f):
            total += 1
            formatted = format_log_line(line)

            ml_anomaly = detector.predict(formatted)
            rule_anomaly = rule_based_anomaly(line)

            is_anomaly = ml_anomaly or rule_anomaly

            if is_anomaly:
                anomalies += 1
                alert_service.log_alert(line.strip(), severity="HIGH")
                print(f"⚠️  ANOMALY [{anomalies}]: {line.strip()}")
            else:
                if total % 50 == 0:
                    print(f"✓ Normal logs processed: {total}")

if __name__ == "__main__":
    main()
