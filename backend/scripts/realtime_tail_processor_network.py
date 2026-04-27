import time
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models.network_anomaly_detector import NetworkAnomalyDetector
from src.services.network_rule_engine import NetworkRuleEngine
from src.services.alert_service import AlertService
from src.config import ALERT_LOG_PATH, NETWORK_MODEL_PATH, NETWORK_SCALER_PATH, NETWORK_SESSIONS_PATH

def main():
    print("🚀 Starting Network Anomaly Detection Processor...")
    
    # Verify all required files exist
    if not Path(NETWORK_MODEL_PATH).exists():
        print(f"❌ Model not found: {NETWORK_MODEL_PATH}")
        print("Run retrain_wireshark_model.py first")
        return
    
    if not Path(NETWORK_SCALER_PATH).exists():
        print(f"❌ Scaler not found: {NETWORK_SCALER_PATH}")
        print("Run wireshark_feature_extractor.py first")
        return
    
    if not Path(NETWORK_SESSIONS_PATH).exists():
        print(f"❌ Sessions file not found: {NETWORK_SESSIONS_PATH}")
        print("Run wireshark_preprocessor.py first")
        return
    
    # Initialize detector, rule engine, alert service
    detector = NetworkAnomalyDetector(NETWORK_MODEL_PATH, NETWORK_SCALER_PATH)
    rule_engine = NetworkRuleEngine()
    alert_service = AlertService(ALERT_LOG_PATH)
    
    # Load sessions
    sessions_path = Path(NETWORK_SESSIONS_PATH)
    with open(sessions_path, 'r') as f:
        sessions = json.load(f)
    
    print(f"📊 Processing {len(sessions)} sessions...")
    
    total_sessions = 0
    anomalies_found = 0
    
    for session in sessions:
        total_sessions += 1
        
        # ML-based detection
        is_ml_anomaly, ml_score = detector.predict(session)
        
        # Rule-based detection
        is_rule_anomaly, rule_severity, rule_reasons = rule_engine.evaluate_session(session)
        
        # Combine: anomaly if either ML or rules trigger
        is_anomaly = is_ml_anomaly or is_rule_anomaly
        
        # Determine final severity
        final_severity = 'LOW'
        if is_ml_anomaly and ml_score < -0.3:
            final_severity = 'HIGH'
        elif is_rule_anomaly:
            final_severity = rule_severity
        
        if is_anomaly:
            anomalies_found += 1
            
            # Format alert
            alert_info = rule_engine.format_alert(session, final_severity, rule_reasons, ml_score)
            alert_text = alert_info['formatted']
            
            # Log alert with correct severity
            metadata = {
                'method': 'ML' if is_ml_anomaly else 'RULES',
                'ml_score': float(ml_score) if is_ml_anomaly else None,
                'rules': rule_reasons,
                'src_ip': session['src_ip'],
                'dst_ip': session['dst_ip']
            }
            
            alert_service.log_alert(alert_text, severity=final_severity, metadata=metadata)
            print(f"⚠️  ANOMALY [{anomalies_found}] [{final_severity}]: {alert_text}")
    
    print(f"\n✅ Processing complete!")
    print(f"   Total sessions: {total_sessions}")
    print(f"   Anomalies detected: {anomalies_found}")
    print(f"   Detection rate: {anomalies_found/max(total_sessions,1)*100:.2f}%")

if __name__ == "__main__":
    main()
