import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

def load_sessions(sessions_path):
    """Load preprocessed sessions"""
    print(f"📖 Loading sessions from {sessions_path}")
    with open(sessions_path, 'r') as f:
        sessions = json.load(f)
    print(f"✓ Loaded {len(sessions)} sessions")
    return sessions

def protocol_to_numeric(protocol_str):
    """Encode protocol as numeric value"""
    protocol_map = {
        'TCP': 1,
        'TLSv1.2': 2,
        'TLSv1.1': 2,
        'TLS': 2,
        'UDP': 3,
        'ICMP': 4,
        'DNS': 5,
        'HTTP': 6,
        'HTTPS': 7,
        'UNKNOWN': 0
    }
    return protocol_map.get(protocol_str, 0)

def is_suspicious_port(port):
    """Flag suspicious ports"""
    if port == -1:
        return 0  # Port not extracted
    
    # Well-known ports for common services
    known_safe = {22, 80, 443, 53, 123, 25, 465, 587, 993, 995, 3306, 5432, 6379, 27017}
    
    # High-numbered ports (>30000) are suspicious from internal networks
    if port > 30000:
        return 1
    
    # Port 0 is invalid
    if port == 0:
        return 1
    
    # Non-standard if not in known
    if port not in known_safe and port > 1024:
        return 1
    
    return 0

def extract_features(sessions):
    """
    Extract minimal but effective features:
    1. packet_count
    2. avg_packet_size
    3. protocol (encoded)
    4. duration
    5. retransmission_ratio
    6. suspicious_src_port
    7. suspicious_dst_port
    8. packet_rate
    """
    print(f"🔧 Extracting features from {len(sessions)} sessions...")
    
    features_list = []
    session_keys = []
    
    for session in sessions:
        try:
            packet_count = session.get('packet_count', 0)
            avg_packet_size = session.get('avg_packet_size', 0)
            protocol = session.get('protocol', 'UNKNOWN')
            duration = session.get('duration', 0)
            retrans_count = session.get('retransmission_count', 0)
            src_port = session.get('src_port', -1)
            dst_port = session.get('dst_port', -1)
            
            # Calculate retransmission ratio
            retrans_ratio = retrans_count / max(packet_count, 1)
            
            # Encode protocol
            protocol_code = protocol_to_numeric(protocol)
            
            # Check port suspicion
            src_port_suspicious = is_suspicious_port(src_port)
            dst_port_suspicious = is_suspicious_port(dst_port)
            
            # Calculate packet rate (packets per second)
            packet_rate = packet_count / max(duration, 0.1)
            
            features = [
                packet_count,
                avg_packet_size,
                protocol_code,
                duration,
                retrans_ratio,
                src_port_suspicious,
                dst_port_suspicious,
                packet_rate
            ]
            
            features_list.append(features)
            session_keys.append((session['src_ip'], session['dst_ip'], session['src_port'], session['dst_port']))
            
        except Exception as e:
            print(f"⚠️  Error extracting features: {e}")
            continue
    
    X = np.array(features_list, dtype=np.float32)
    print(f"✓ Extracted {len(X)} feature vectors")
    
    return X, session_keys

def normalize_features(X):
    """Normalize features using StandardScaler"""
    print(f"📊 Normalizing {len(X)} feature vectors...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"✓ Normalized features")
    return X_scaled, scaler

def main():
    sessions_path = Path(__file__).resolve().parent.parent / "data" / "wireshark_sessions.json"
    features_output = Path(__file__).resolve().parent.parent / "data" / "wireshark_features.npy"
    scaler_path = Path(__file__).resolve().parent.parent / "models" / "network_scaler.joblib"
    
    if not sessions_path.exists():
        print(f"❌ Sessions file not found: {sessions_path}")
        print("Run wireshark_preprocessor.py first")
        return
    
    # Load sessions
    sessions = load_sessions(sessions_path)
    
    # Extract features
    X, session_keys = extract_features(sessions)
    
    # Normalize
    X_scaled, scaler = normalize_features(X)
    
    # Save
    np.save(features_output, X_scaled)
    joblib.dump(scaler, scaler_path)
    
    print(f"💾 Saved features to {features_output}")
    print(f"💾 Saved scaler to {scaler_path}")
    print("✅ Feature extraction complete!")

if __name__ == "__main__":
    main()
