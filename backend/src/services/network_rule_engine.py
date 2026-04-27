from datetime import datetime

class NetworkRuleEngine:
    """
    Lightweight rule-based detection for network anomalies.
    Checks for known attack patterns in network traffic.
    Assigns severity: HIGH (critical threats), MEDIUM (suspicious patterns), LOW (minor issues)
    """
    
    # Suspicious port ranges
    WELL_KNOWN_PORTS = {22, 80, 443, 53, 123, 25, 465, 587, 993, 995, 3306, 5432, 6379, 27017}
    HIGH_RISK_PORTS = {135, 139, 445, 1433, 3389}  # Windows RPC, SMB, RDP, MSSQL
    
    # Thresholds (adjusted for severity levels)
    CRITICAL_PACKET_RATE = 500    # packets/sec - indicates DDoS/flooding
    HIGH_PACKET_RATE = 200         # packets/sec - suspicious bulk transfer
    MEDIUM_PACKET_RATE = 100       # packets/sec - moderate activity
    CRITICAL_RETRANS_THRESHOLD = 0.5   # 50% retransmissions - severe network issue
    HIGH_RETRANS_THRESHOLD = 0.3       # 30% - clear issue
    MEDIUM_RETRANS_THRESHOLD = 0.15    # 15% - moderate concern
    
    def __init__(self):
        self.alerts = []
    
    def check_high_packet_rate(self, session_dict):
        """Flag if packet rate is unusually high - assign severity based on rate"""
        packet_rate = session_dict.get('packet_rate', 0)
        
        if packet_rate > self.CRITICAL_PACKET_RATE:
            return 'HIGH', f"Critical packet rate: {packet_rate:.2f} packets/sec (possible DDoS)"
        elif packet_rate > self.HIGH_PACKET_RATE:
            return 'HIGH', f"High packet rate: {packet_rate:.2f} packets/sec"
        elif packet_rate > self.MEDIUM_PACKET_RATE:
            return 'MEDIUM', f"Moderate packet rate: {packet_rate:.2f} packets/sec"
        
        return None, None
    
    def check_retransmission_spike(self, session_dict):
        """Flag if retransmission ratio is high - assign severity based on ratio"""
        retrans_ratio = session_dict.get('retransmission_ratio', 0)
        
        if retrans_ratio > self.CRITICAL_RETRANS_THRESHOLD:
            return 'HIGH', f"Severe retransmission spike: {retrans_ratio:.2%} (network highly unstable)"
        elif retrans_ratio > self.HIGH_RETRANS_THRESHOLD:
            return 'HIGH', f"High retransmission ratio: {retrans_ratio:.2%}"
        elif retrans_ratio > self.MEDIUM_RETRANS_THRESHOLD:
            return 'MEDIUM', f"Elevated retransmission ratio: {retrans_ratio:.2%}"
        
        return None, None
    
    def check_suspicious_ports(self, session_dict):
        """Flag connections to suspicious ports - assign severity based on port"""
        src_port = session_dict.get('src_port', -1)
        dst_port = session_dict.get('dst_port', -1)
        
        # High-risk destination ports (Windows administrative services)
        if dst_port in self.HIGH_RISK_PORTS:
            return 'HIGH', f"Connection to high-risk port: {dst_port} (Windows admin service)"
        
        # High-numbered destination ports from internal networks (possible C2 or data exfil)
        if dst_port > 30000:
            return 'MEDIUM', f"Connection to unusual high port: {dst_port}"
        
        # Non-standard source port (unusual but lower priority)
        if src_port > 1024 and src_port not in {3000, 5000, 8000, 8080, 9000, 9090}:
            return 'LOW', f"Non-standard source port: {src_port}"
        
        return None, None
    
    def check_port_scanning(self, sessions_list):
        """
        Flag if single source is connecting to many different ports.
        Signature of port scanning attack.
        """
        # Group by source IP
        src_to_dst_ports = {}
        for session in sessions_list:
            src_ip = session.get('src_ip')
            dst_port = session.get('dst_port', -1)
            
            if src_ip:
                if src_ip not in src_to_dst_ports:
                    src_to_dst_ports[src_ip] = set()
                if dst_port > 0:
                    src_to_dst_ports[src_ip].add(dst_port)
        
        # Flag IPs scanning many ports
        suspicious_sources = {}
        for src_ip, ports in src_to_dst_ports.items():
            if len(ports) > 20:  # Connecting to >20 different ports = likely scanning
                suspicious_sources[src_ip] = ('HIGH', len(ports), 'Port scan detected')
            elif len(ports) > 10:  # Medium concern
                suspicious_sources[src_ip] = ('MEDIUM', len(ports), 'Elevated port connectivity')
        
        return suspicious_sources
    
    def evaluate_session(self, session_dict):
        """
        Evaluate a single session and return rule-based anomaly flag with severity.
        Returns: (is_anomaly, severity, reasons)
        severity: 'HIGH' (critical), 'MEDIUM' (suspicious), 'LOW' (minor)
        """
        reasons = []
        detected_severities = []
        
        # Calculate additional metrics from session data
        packet_count = session_dict.get('packet_count', 0)
        duration = session_dict.get('duration', 0)
        retrans_count = session_dict.get('retransmission_count', 0)
        
        # Add computed metrics to session dict for rule checking
        session_with_metrics = dict(session_dict)
        session_with_metrics['packet_rate'] = packet_count / max(duration, 0.1)
        session_with_metrics['retransmission_ratio'] = retrans_count / max(packet_count, 1)
        
        # Check each rule
        check_functions = [
            ('packet_rate', self.check_high_packet_rate),
            ('retransmission', self.check_retransmission_spike),
            ('suspicious_ports', self.check_suspicious_ports),
        ]
        
        for rule_name, check_func in check_functions:
            try:
                result = check_func(session_with_metrics)
                if result[0]:  # If severity is returned (not None)
                    severity, reason = result
                    detected_severities.append(severity)
                    reasons.append(reason)
            except Exception as e:
                print(f"⚠️  Error in rule {rule_name}: {e}")
        
        is_anomaly = len(reasons) > 0
        
        # Use highest severity detected
        final_severity = 'LOW'
        if 'HIGH' in detected_severities:
            final_severity = 'HIGH'
        elif 'MEDIUM' in detected_severities:
            final_severity = 'MEDIUM'
        
        return is_anomaly, final_severity, reasons
    
    def format_alert(self, session_dict, rule_severity, rule_reasons, ml_confidence=None):
        """Format rule-based alert for logging in CSV format compatible with frontend parser"""
        from datetime import datetime
        
        timestamp = datetime.now().isoformat()
        src_ip = session_dict.get('src_ip', 'N/A')
        dst_ip = session_dict.get('dst_ip', 'N/A')
        src_port = session_dict.get('src_port', 'N/A')
        dst_port = session_dict.get('dst_port', 'N/A')
        protocol = session_dict.get('protocol', 'UNKNOWN')
        reason = rule_reasons[0] if rule_reasons else 'Anomaly detected'
        
        # Format as CSV to match realtime_logs.txt structure:
        # timestamp,IP,method,status,browser,location,action
        # For network anomalies: timestamp,src_ip,protocol,dst_port,severity,dst_ip,reason
        alert_csv = f"{timestamp},{src_ip},{protocol},{rule_severity},{reason[:50]},{dst_ip},{src_port}→{dst_port}"
        
        # Readable format for console/alerts panel display
        alert_readable = f"{src_ip}:{src_port} → {dst_ip}:{dst_port} [{protocol}] - {reason}"
        
        return {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'reasons': rule_reasons,
            'severity': rule_severity,
            'ml_score': ml_confidence,
            'formatted': alert_csv  # Use CSV format for logging
        }
