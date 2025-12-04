from .network import PortScanner
from .fingerprint import ServiceIdentifier
from .vulnerability import VulnDatabase
import time

class TitanReconCore:
    def __init__(self):
        print("[*] RECON GRID: INITIALIZING SUB-SYSTEMS...")
        self.scanner = PortScanner()
        self.fp = ServiceIdentifier()
        self.vuln = VulnDatabase()
        
        # Common Ports Profile
        self.target_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080, 8443]

    def run_full_scan(self, target_ip):
        print(f"\n[*] INITIATING VULNERABILITY ASSESSMENT ON {target_ip}...")
        time.sleep(1)
        
        # 1. Network Scan
        print(f"    > Scanning {len(self.target_ports)} ports (TCP Connect)...")
        open_ports = self.scanner.scan_target(target_ip, self.target_ports)
        
        if not open_ports:
            print("    [-] Host appears down or firewalled.")
            return

        print(f"    [+] {len(open_ports)} Ports Open.")
        
        # 2. Fingerprinting & CVE Lookup
        for port, banner in open_ports:
            # Clean banner
            clean_banner = banner.split('\n')[0][:40] 
            service = self.fp.identify(clean_banner)
            cves = self.vuln.check_cves(service)
            
            print(f"\n    [PORT {port}] {service}")
            print(f"        > Raw Banner: {clean_banner}")
            
            if cves:
                print(f"\033[1;31m        > VULNERABILITIES DETECTED:\033[0m")
                for cve in cves:
                    print(f"\033[1;31m          - {cve}\033[0m")
            else:
                print("        > No known CVEs in local database.")

        print("\n[*] SCAN COMPLETE.")
