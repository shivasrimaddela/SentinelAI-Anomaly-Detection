import joblib
from pathlib import Path

class AnomalyDetector:
    def __init__(self, model_path, vectorizer_path):
        self.model = joblib.load(Path(model_path))
        self.vectorizer = joblib.load(Path(vectorizer_path))

    def predict(self, log_line: str) -> bool:
        X = self.vectorizer.transform([log_line])
        return self.model.predict(X)[0] == -1
