import joblib
from pathlib import Path
import numpy as np

class NetworkAnomalyDetector:
    """
    Detector for network packet anomalies using trained Isolation Forest.
    Works with aggregated session features.
    """
    
    def __init__(self, model_path, scaler_path):
        self.model = joblib.load(Path(model_path))
        self.scaler = joblib.load(Path(scaler_path))
        print("✓ Network detector loaded")
    
    def extract_features_from_session(self, session_dict):
        """
        Convert a session dict to feature vector.
        Must match the format used in training.
        """
        def protocol_to_numeric(protocol_str):
            protocol_map = {
                'TCP': 1, 'TLSv1.2': 2, 'TLSv1.1': 2, 'TLS': 2,
                'UDP': 3, 'ICMP': 4, 'DNS': 5, 'HTTP': 6, 'HTTPS': 7,
                'UNKNOWN': 0
            }
            return protocol_map.get(protocol_str, 0)
        
        def is_suspicious_port(port):
            if port == -1:
                return 0
            known_safe = {22, 80, 443, 53, 123, 25, 465, 587, 993, 995, 3306, 5432, 6379, 27017}
            if port > 30000:
                return 1
            if port == 0:
                return 1
            if port not in known_safe and port > 1024:
                return 1
            return 0
        
        packet_count = session_dict.get('packet_count', 0)
        avg_packet_size = session_dict.get('avg_packet_size', 0)
        protocol = session_dict.get('protocol', 'UNKNOWN')
        duration = session_dict.get('duration', 0)
        retrans_count = session_dict.get('retransmission_count', 0)
        src_port = session_dict.get('src_port', -1)
        dst_port = session_dict.get('dst_port', -1)
        
        retrans_ratio = retrans_count / max(packet_count, 1)
        protocol_code = protocol_to_numeric(protocol)
        src_port_suspicious = is_suspicious_port(src_port)
        dst_port_suspicious = is_suspicious_port(dst_port)
        packet_rate = packet_count / max(duration, 0.1)
        
        features = np.array([[
            packet_count,
            avg_packet_size,
            protocol_code,
            duration,
            retrans_ratio,
            src_port_suspicious,
            dst_port_suspicious,
            packet_rate
        ]], dtype=np.float32)
        
        return features
    
    def predict(self, session_dict):
        """
        Predict if session is anomalous.
        Returns: (is_anomaly, confidence_score)
        is_anomaly: True if -1 (anomaly), False if 1 (normal)
        """
        try:
            # Extract and scale features
            features = self.extract_features_from_session(session_dict)
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            
            # Get decision function (higher = more anomalous)
            score = self.model.decision_function(features_scaled)[0]
            
            is_anomaly = (prediction == -1)
            
            return is_anomaly, score
        
        except Exception as e:
            print(f"⚠️  Error in prediction: {e}")
            return False, 0.0
