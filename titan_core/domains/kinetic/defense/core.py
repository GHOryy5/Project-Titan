from .cde import CollateralDamageEngine
from .interceptor import KineticInterceptor
from .iads import EnemyIADS
from titan_core.utils.geo import GeoMath # <--- USING SHARED LIB
import time

class TitanDefenseCore:
    def __init__(self):
        print("\033[1;34m[*] TITAN DEFENSE v3.0 (ENTERPRISE): LINKED TO UTILS...\033[0m")
        self.cde = CollateralDamageEngine()
        self.interceptor = KineticInterceptor()
        self.iads = EnemyIADS()

    def scan_airspace(self, target_lat, target_long):
        print(f"\n[*] DEFENSE MATRIX ACTIVATED FOR SECTOR {target_lat:.4f}, {target_long:.4f}")
        time.sleep(1)
        
        # Logic is similar, but relies on shared libraries in background
        threat_status = self.iads.ping_network(target_lat)
        
        if threat_status == "MISSILE_LAUNCH":
            print("\n\033[1;41m[!] INCOMING THREAT DETECTED [!]\033[0m")
            can_intercept = self.interceptor.launch_solution(5000, 12000)
            
            if can_intercept:
                is_safe, code = self.cde.evaluate_strike_safety(target_lat, target_long)
                if is_safe:
                    return "THREAT_DESTROYED", 0, "SAFE"
                else:
                    print("    [C2] AUTO-ABORT: CIVILIAN RISK TOO HIGH.")
                    return "JAMMING_ENGAGED", 0, "SAFE"
        else:
            print("    [STATUS] Airspace Contested but no active launches.")
        return None, 0, "SAFE"
