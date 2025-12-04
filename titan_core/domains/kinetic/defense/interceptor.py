import math
import time

class KineticInterceptor:
    def __init__(self):
        print("[*] DEFENSE GRID: INTERCEPTOR GUIDANCE ONLINE")
        self.max_g = 40.0 # High maneuverability
        self.velocity = 900.0 # m/s (Mach 3)

    def launch_solution(self, threat_alt, threat_range):
        """
        Simulates the Proportional Navigation (PropNav) calculation.
        """
        print(f"    [GUIDANCE] Computing Fire Control Solution...")
        print(f"        > Threat Altitude: {threat_alt}m")
        print(f"        > Threat Range:    {threat_range}m")
        
        # Physics: Time to Intercept
        # Simple kinematic: t = dist / v_closing
        v_closing = self.velocity + 300 # Assume target coming at 300m/s
        tti = threat_range / v_closing
        
        print(f"        > Closing Velocity: {v_closing} m/s")
        print(f"        > Time to Intercept: {tti:.2f}s")
        
        if tti < 2.0:
            print("\033[1;31m        [!] WARNING: MINIMUM RANGE VIOLATION. IMPOSSIBLE INTERCEPT.\033[0m")
            return False
            
        print("    [GUIDANCE] Tube 1: LOCKED. Tube 2: LOCKED.")
        return True

    def simulate_flight(self):
        print("    [INTERCEPTOR] TAMIR MISSILE LAUNCHED...")
        # Animation
        for i in range(3):
            print(f"        > TRACKING... [Corrections: {math.sin(i)*10:.2f} deg]")
            time.sleep(0.4)
        print("\033[1;32m    [+] HARD KILL CONFIRMED. TARGET DESTROYED.\033[0m")
