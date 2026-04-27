import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

def load_features():
    """Load extracted features"""
    features_path = Path(__file__).resolve().parent.parent / "data" / "wireshark_features.npy"
    
    if not features_path.exists():
        print(f"❌ Features file not found: {features_path}")
        print("Run wireshark_feature_extractor.py first")
        return None
    
    X = np.load(features_path)
    print(f"📖 Loaded {len(X)} feature vectors")
    return X

def train_isolation_forest(X):
    """
    Train Isolation Forest on network features.
    Using similar parameters as original model.
    """
    print(f"🤖 Training Isolation Forest on {len(X)} samples...")
    
    model = IsolationForest(
        n_estimators=150,
        contamination=0.15,  # Expect ~15% anomalies in network traffic
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X)
    print("✓ Training complete")
    
    return model

def evaluate_model(model, X):
    """Get basic stats about model predictions"""
    predictions = model.predict(X)
    anomaly_count = (predictions == -1).sum()
    normal_count = (predictions == 1).sum()
    anomaly_ratio = anomaly_count / len(X) * 100
    
    print(f"\n📊 Model Predictions:")
    print(f"   Normal samples: {normal_count}")
    print(f"   Anomaly samples: {anomaly_count}")
    print(f"   Anomaly ratio: {anomaly_ratio:.2f}%")

def main():
    model_path = Path(__file__).resolve().parent.parent / "models" / "network_isolation_model.joblib"
    
    # Load features
    X = load_features()
    if X is None:
        return
    
    # Train
    model = train_isolation_forest(X)
    
    # Evaluate
    evaluate_model(model, X)
    
    # Save
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"\n💾 Saved model to {model_path}")
    print("✅ Model retraining complete!")

if __name__ == "__main__":
    main()
