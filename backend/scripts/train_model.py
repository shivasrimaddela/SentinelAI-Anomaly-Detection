import sys
from pathlib import Path

# 🔧 IMPORTANT: add backend root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest

from src.utils import format_log_line
from src.config import TRAINING_LOG_PATH, MODEL_PATH, VECTORIZER_PATH

# Load training log lines
with open(TRAINING_LOG_PATH, "r", encoding="utf-8") as f:
    logs = [format_log_line(line) for line in f if line.strip()]

print(f"Loaded {len(logs)} training logs")

# Train vectorizer
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(logs)

# Train model
model = IsolationForest(
    n_estimators=150,
    contamination=0.2,
    random_state=42
)
model.fit(X)

# Ensure model directory exists
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# Save model
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("✅ Model training completed successfully")
