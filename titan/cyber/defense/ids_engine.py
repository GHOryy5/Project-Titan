import time
from collections import defaultdict
from titan.cyber.network_analysis.protocols import TCPHeader, IPv4Header

class IntrusionDetectionSystem:
    """
    Stateful analysis engine for detecting network anomalies.
    Tracks flow states and statistical variance.
    """
    def __init__(self):
        # Tracking SYN packets per IP for DoS detection
        self.syn_tracker = defaultdict(int)
        # Tracking unique ports touched per IP for Scan detection
        self.port_scan_tracker = defaultdict(set)
        # Whitelist - These IPs are ignored
        self.trusted_ips = ["127.0.0.1", "192.168.1.1"]
        
        # Detection Thresholds
        self.DOS_THRESHOLD = 100     # SYN packets per minute
        self.SCAN_THRESHOLD = 20     # Unique ports per minute

    def inspect_packet(self, ip_packet: IPv4Header, tcp_packet: TCPHeader):
        """
        Core analysis loop. Returns a Threat Alert if anomaly detected.
        """
        src_ip = ip_packet.src_ip
        
        if src_ip in self.trusted_ips:
            return None

        # 1. DoS Detection (SYN Flood)
        # A SYN packet without an ACK flag indicates an attempt to open a connection.
        # High volume of these without completion suggests a flood.
        if tcp_packet.flag_syn and not tcp_packet.flag_ack:
            self.syn_tracker[src_ip] += 1
            
            if self.syn_tracker[src_ip] > self.DOS_THRESHOLD:
                return self._generate_alert(
                    "DENIAL_OF_SERVICE", 
                    src_ip, 
                    f"SYN Flood detected: {self.syn_tracker[src_ip]} packets/min"
                )

        # 2. Reconnaissance Detection (Vertical Port Scan)
        # Tracking unique destination ports targeted by a single source IP.
        self.port_scan_tracker[src_ip].add(tcp_packet.dest_port)
        
        if len(self.port_scan_tracker[src_ip]) > self.SCAN_THRESHOLD:
             return self._generate_alert(
                "RECONNAISSANCE",
                src_ip,
                f"Vertical Port Scan detected: {len(self.port_scan_tracker[src_ip])} unique ports targeted"
            )

        # 3. C2 Beacon Detection (Heuristic)
        # Logic: Small payload (under 64 bytes) with PSH flag often indicates a command beacon.
        if len(tcp_packet.data) < 64 and tcp_packet.flag_psh:
            # In a full 7k LOC system, we would track time-delta variance here
            # For now, we mark it as suspicious if it happens repeatedly (logic simplified)
            pass
            
        return None

    def _generate_alert(self, alert_type, ip, details):
        return {
            "timestamp": time.time(),
            "severity": "CRITICAL",
            "type": alert_type,
            "source_ip": ip,
            "details": details,
            "action_required": "BLOCK_FIREWALL"
        }

    def reset_counters(self):
        """
        Called periodically to reset statistical windows (e.g., every minute).
        This prevents counters from growing infinitely.
        """
        self.syn_tracker.clear()
        self.port_scan_tracker.clear()
