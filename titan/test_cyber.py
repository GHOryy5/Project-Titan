import struct
import time
import random
from titan.cyber.network_analysis.protocols import EthernetFrame, IPv4Header, TCPHeader
from titan.cyber.defense.ids_engine import IntrusionDetectionSystem

def generate_syn_packet(src_ip_str, dst_ip_str, src_port, dst_port):
    """
    Constructs a raw binary TCP SYN packet manually.
    This mimics the raw bytes a network card receives.
    """
    # Helper to pack IP string to bytes (e.g., "192.168.1.1" -> b'\xc0\xa8\x01\x01')
    def ip_to_bytes(ip):
        return bytes(map(int, ip.split('.')))

    # 1. Build TCP Header (20 bytes)
    # Source Port, Dest Port, Seq, Ack, Offset/Flags (SYN=2), Window, Checksum, UrgPtr
    # Flags: 0x5002 -> Data Offset 5 (5 * 4 = 20 bytes header), Flags: SYN (0x02)
    tcp_header = struct.pack('!HHLLHHHH', 
        src_port, dst_port, 
        random.randint(0, 2**32), 0, 
        0x5002, 
        5840, 0, 0
    )

    # 2. Build IP Header (20 bytes)
    # Ver/IHL (0x45), TOS, Len, ID, Frag, TTL, Proto(TCP=6), Checksum, Src, Dst
    ip_header = struct.pack('!BBHHHBBH4s4s', 
        69, 0, 40, 54321, 0, 64, 6, 0, 
        ip_to_bytes(src_ip_str), 
        ip_to_bytes(dst_ip_str)
    )

    # 3. Build Ethernet Header (14 bytes)
    # Dest Mac, Src Mac, Proto (IPv4 = 0x0800)
    eth_header = struct.pack('!6s6sH', 
        b'\xaa\xaa\xaa\xaa\xaa\xaa', 
        b'\xbb\xbb\xbb\xbb\xbb\xbb', 
        0x0800
    )

    # Combine into a single binary blob
    return eth_header + ip_header + tcp_header

def run_simulation():
    print("[*] TITAN CYBER DEFENSE SYSTEM INITIALIZING...")
    
    ids = IntrusionDetectionSystem()
    attacker_ip = "10.88.99.14"
    target_ip = "192.168.1.5"
    
    print(f"[SIM] Simulating SYN Flood attack from {attacker_ip}...")
    
    # Simulate 150 packets hitting the interface rapidly
    for i in range(150):
        # Generate raw binary data
        raw_data = generate_syn_packet(attacker_ip, target_ip, 4444, 80)
        
        # --- THE PARSING PIPELINE ---
        # 1. Layer 2: Ethernet
        eth = EthernetFrame(raw_data)
        
        # 2. Layer 3: IP
        if eth.proto == 8: # IPv4
            ipv4 = IPv4Header(eth.data)
            
            # 3. Layer 4: TCP
            if ipv4.proto == 6:
                tcp = TCPHeader(ipv4.data)
                
                # 4. IDS Analysis
                alert = ids.inspect_packet(ipv4, tcp)
                
                if alert:
                    print(f"\n[!!!] IDS ALERT TRIGGERED!")
                    print(f"TYPE: {alert['type']}")
                    print(f"DETAILS: {alert['details']}")
                    print(f"ACTION: {alert['action_required']}")
                    break
        
        if i % 20 == 0:
            print(f"  Processed {i} packets...", end="\r")

if __name__ == "__main__":
    run_simulation()
