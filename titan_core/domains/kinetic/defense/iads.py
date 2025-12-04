import random
import time

class EnemyIADS:
    """
    Simulates the Enemy's Integrated Air Defense System.
    If one radar sees you, it alerts the others via Data Link.
    """
    def __init__(self):
        print("[*] DEFENSE GRID: ENEMY THREAT EMITTER SIMULATION ONLINE")
        self.network = {
            "NODE_A": {"type": "EARLY_WARNING", "freq": 150, "range": 200},
            "NODE_B": {"type": "SA-6 TRACKER",  "freq": 8500, "range": 25},
            "NODE_C": {"type": "ZSU-23 OPTICAL", "freq": 0, "range": 5}
        }
        self.alert_state = "GREEN"

    def ping_network(self, user_lat):
        """
        Simulates the enemy network reacting to the user's presence.
        """
        # Logic: If user is deep (lat > 0.05), early warning triggers
        if user_lat > 0.05:
            if self.alert_state == "GREEN":
                print("\033[1;33m    [IADS] DETECTED: Enemy 'Spoon Rest' Radar picked up signature.\033[0m")
                self.alert_state = "YELLOW"
                print("    [IADS] Data Link: Handoff to Tracking Radars...")
                time.sleep(1)
                
        if user_lat > 0.08 and self.alert_state == "YELLOW":
            print("\033[1;31m    [IADS] LOCK-ON: SA-6 'Straight Flush' has acquired target.\033[0m")
            self.alert_state = "RED"
            return "MISSILE_LAUNCH"
            
        return "TRACKING"
