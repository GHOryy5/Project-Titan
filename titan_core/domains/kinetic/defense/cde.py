import math
from dataclasses import dataclass

@dataclass
class ProtectedZone:
    id: str
    lat: float
    long: float
    radius: float
    type: str  # HOSPITAL, SCHOOL, RELIGIOUS

class CollateralDamageEngine:
    def __init__(self):
        print("[*] DEFENSE GRID: CDE SUBSYSTEM LOADED")
        # The Human Terrain Database
        self.zones = [
            ProtectedZone("CIV_VILLAGE_ALPHA", 0.005, 0.005, 500, "RESIDENTIAL"),
            ProtectedZone("MSF_HOSPITAL", 0.002, 0.008, 200, "HOSPITAL"),
            ProtectedZone("CENTRAL_MOSQUE", 0.001, 0.001, 150, "RELIGIOUS")
        ]
        self.lethal_radius_missile = 40.0 # meters

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Haversine approximation for short distances (flat earth calc for speed)
        # 1 deg lat = 111,000 meters
        dx = (lat2 - lat1) * 111000
        dy = (lon2 - lon1) * 111000
        return math.sqrt(dx**2 + dy**2)

    def evaluate_strike_safety(self, target_lat, target_long):
        """
        Determines if a defensive intercept will cause civilian harm.
        """
        print(f"    [CDE] Analyzing Debris Field for Impact at {target_lat:.4f}, {target_long:.4f}...")
        
        for zone in self.zones:
            dist = self.calculate_distance(zone.lat, zone.long, target_lat, target_long)
            
            # Risk Logic
            if dist < (zone.radius + self.lethal_radius_missile + 100):
                # TOO CLOSE
                print(f"\033[1;31m    [!] CDE VIOLATION: Intercept would shower {zone.type} ({zone.id}) with debris.\033[0m")
                print(f"        > Distance: {dist:.1f}m | Safe Margin: {zone.radius + 140}m")
                return False, f"ROE_HARD_BLOCK_{zone.id}"
                
        print("\033[1;32m    [+] CDE CHECK PASSED: Low Collateral Risk.\033[0m")
        return True, "CLEARED_HOT"
