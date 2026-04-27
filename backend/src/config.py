import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
LOG_PATH = DATA_DIR / "realtime_logs.txt"
TRAINING_LOG_PATH = DATA_DIR / "sample_training_logs.txt"
ALERT_LOG_PATH = DATA_DIR / "alerts.log"

# Model paths
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "isoforest_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"

# Network/Wireshark model paths
NETWORK_MODEL_PATH = MODELS_DIR / "network_isolation_model.joblib"
NETWORK_SCALER_PATH = MODELS_DIR / "network_scaler.joblib"
NETWORK_SESSIONS_PATH = DATA_DIR / "wireshark_sessions.json"
WIRESHARK_XLS_PATH = DATA_DIR / "wire shark sample dataset.xls"

# Model parameters
ISOFOR_ESTIMATORS = 150
ISOFOR_CONTAMINATION = 0.20

# Flask settings
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 8000
FLASK_DEBUG = True

# CORS settings
CORS_ORIGINS = ["http://localhost:3000"]

# Notification settings
ENABLE_EMAIL_ALERTS = False
ENABLE_SLACK_ALERTS = False
SLACK_WEBHOOK_URL = ""

# Streaming settings
ENABLE_WEBSOCKET = True
STREAM_INTERVAL = 2  # seconds
