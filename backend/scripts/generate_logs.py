import time
import random
from datetime import datetime

NORMAL_ACTIONS = ["visit", "click", "browse"]
ANOMALY_ACTIONS = [
    "port_scan",
    "bruteforce",
    "sql_injection",
    "xss_attack",
    "data_exfiltration",
    "unauthorized_admin_access"
]

METHODS = ["GET", "POST", "PUT", "DELETE"]
BROWSERS = ["Chrome", "Firefox", "Safari", "Edge", "Bot"]
LOCATIONS = ["India", "USA", "France", "Brazil", "Canada", "China", "Russia"]

NORMAL_STATUS = ["200", "301"]
ANOMALY_STATUS = ["401", "403", "404", "500"]

NORMAL_IP_RANGE = "192.168.0."
ANOMALY_IPS = [
    "45.33.32.156",
    "103.221.244.12",
    "185.234.219.10",
    "91.240.118.172"
]

LOG_FILE = "data/realtime_logs.txt"

def generate_normal_log():
    return (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},"
        f"{NORMAL_IP_RANGE}{random.randint(1, 254)},"
        f"{random.choice(METHODS)},"
        f"{random.choice(NORMAL_STATUS)},"
        f"{random.choice(BROWSERS[:-1])},"
        f"{random.choice(LOCATIONS)},"
        f"{random.choice(NORMAL_ACTIONS)}\n"
    )

def generate_anomaly_log():
    return (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},"
        f"{random.choice(ANOMALY_IPS)},"
        f"{random.choice(METHODS)},"
        f"{random.choice(ANOMALY_STATUS)},"
        f"Bot,"
        f"{random.choice(['China', 'Russia'])},"
        f"{random.choice(ANOMALY_ACTIONS)}\n"
    )

print("Log generator started (normal + anomaly logs)")

with open(LOG_FILE, "a", encoding="utf-8") as f:
    while True:
        # 80% normal, 20% anomaly
        if random.random() < 0.8:
            log = generate_normal_log()
        else:
            # burst anomalies
            for _ in range(random.randint(2, 4)):
                log = generate_anomaly_log()
                f.write(log)
                f.flush()
                time.sleep(0.3)
            continue

        f.write(log)
        f.flush()
        time.sleep(1)
