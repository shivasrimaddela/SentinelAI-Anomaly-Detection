import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import json
import re
from collections import defaultdict
from datetime import datetime

def extract_ports_from_info(info_str):
    """
    Extract source and destination ports from Wireshark Info field.
    Examples:
    - "59850 > 7680 [SYN]" -> (59850, 7680)
    - "58762 > 443 [ACK]" -> (58762, 443)
    - "443 > 58762 [ACK]" -> (443, 58762)
    - "Application Data" -> (None, None)
    """
    if not isinstance(info_str, str):
        return None, None
    
    # Pattern: number > number
    match = re.search(r'(\d+)\s*>\s*(\d+)', info_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def is_retransmission(info_str):
    """Check if packet is a retransmission"""
    if not isinstance(info_str, str):
        return False
    return bool(re.search(r'\[TCP Retransmission\]|\[TCP Dup ACK', info_str))

def read_wireshark_xls(xls_path):
    """Read Wireshark file (may be XLS, XLSX, or CSV with XLS extension)"""
    print(f"📖 Reading Wireshark file: {xls_path}")
    try:
        # Try as CSV first (Wireshark export can be CSV with .xls extension)
        df = pd.read_csv(xls_path)
        print(f"✓ Read as CSV - Loaded {len(df)} packets")
        return df
    except:
        try:
            # Try with openpyxl (for .xlsx)
            df = pd.read_excel(xls_path, engine='openpyxl')
            print(f"✓ Read as XLSX - Loaded {len(df)} packets")
            return df
        except:
            try:
                # Fallback to xlrd (for old XLS)
                df = pd.read_excel(xls_path, engine='xlrd')
                print(f"✓ Read as XLS - Loaded {len(df)} packets")
                return df
            except Exception as e:
                print(f"❌ Could not read file: {e}")
                raise

def aggregate_into_sessions(df):
    """
    Aggregate packets into sessions.
    Session = unique (Source IP, Dest IP, Source Port, Dest Port, Protocol)
    """
    sessions = defaultdict(lambda: {
        'packets': [],
        'packet_count': 0,
        'total_length': 0,
        'retransmission_count': 0,
        'times': [],
        'protocols': set()
    })
    
    print(f"🔄 Aggregating {len(df)} packets into sessions...")
    
    for idx, row in df.iterrows():
        try:
            src_ip = str(row.get('Source', '')).strip()
            dst_ip = str(row.get('Destination', '')).strip()
            protocol = str(row.get('Protocol', 'UNKNOWN')).strip()
            length = float(row.get('Length', 0))
            time_val = float(row.get('Time', 0))
            info_str = str(row.get('Info', ''))
            
            # Skip malformed rows
            if not src_ip or not dst_ip or src_ip == 'nan' or dst_ip == 'nan':
                continue
            
            # Extract ports
            src_port, dst_port = extract_ports_from_info(info_str)
            retrans = is_retransmission(info_str)
            
            # Create session key
            session_key = (src_ip, dst_ip, src_port, dst_port, protocol)
            
            # Update session
            session = sessions[session_key]
            session['packets'].append(row.to_dict())
            session['packet_count'] += 1
            session['total_length'] += length
            session['times'].append(time_val)
            session['protocols'].add(protocol)
            if retrans:
                session['retransmission_count'] += 1
        
        except Exception as e:
            print(f"⚠️  Skipped row {idx}: {e}")
            continue
    
    print(f"✓ Created {len(sessions)} sessions")
    return sessions

def clean_sessions(sessions):
    """
    Remove duplicate sessions and handle anomalies.
    Keep sessions with reasonable data.
    """
    print(f"🧹 Cleaning sessions...")
    cleaned = {}
    
    for session_key, session_data in sessions.items():
        # Skip single-packet sessions (likely noise)
        if session_data['packet_count'] < 1:
            continue
        
        # Skip invalid sessions
        if session_data['total_length'] <= 0:
            continue
        
        # Calculate duration
        if len(session_data['times']) > 1:
            duration = max(session_data['times']) - min(session_data['times'])
        else:
            duration = 0
        
        # Calculate average packet size
        avg_size = session_data['total_length'] / session_data['packet_count']
        
        # Skip if packet size is unrealistic
        if avg_size > 65535 or avg_size < 20:
            continue
        
        cleaned[session_key] = {
            **session_data,
            'duration': duration,
            'avg_packet_size': avg_size,
            'protocols': list(session_data['protocols'])
        }
    
    print(f"✓ After cleaning: {len(cleaned)} sessions")
    return cleaned

def save_sessions(sessions, output_path):
    """Save aggregated sessions as JSON (serializable format)"""
    # Convert to serializable format
    sessions_list = []
    for (src_ip, dst_ip, src_port, dst_port, protocol), session_data in sessions.items():
        sessions_list.append({
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port if src_port else -1,
            'dst_port': dst_port if dst_port else -1,
            'protocol': protocol,
            **{k: v for k, v in session_data.items() if k != 'packets'}
        })
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(sessions_list, f, indent=2)
    
    print(f"💾 Saved {len(sessions_list)} sessions to {output_path}")
    return len(sessions_list)

def main():
    xls_path = Path(__file__).resolve().parent.parent / "data" / "wire shark sample dataset.xls"
    output_path = Path(__file__).resolve().parent.parent / "data" / "wireshark_sessions.json"
    
    # Check if file exists
    if not xls_path.exists():
        print(f"❌ File not found: {xls_path}")
        return
    
    # Read
    df = read_wireshark_xls(xls_path)
    
    # Aggregate
    sessions = aggregate_into_sessions(df)
    
    # Clean
    cleaned_sessions = clean_sessions(sessions)
    
    # Save
    save_sessions(cleaned_sessions, output_path)
    
    print("✅ Preprocessing complete!")

if __name__ == "__main__":
    main()
