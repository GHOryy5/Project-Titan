import math
import random
import time

class TitanHunter:
    def __init__(self):
        self.c = 299792458 # Speed of light
        self.towers = {"A": (0,0), "B": (15000,0), "C": (7500, 13000)}

    def track_target(self, target_id):
        print(f"[*] ACTIVATING TDoA GRID FOR TARGET: {target_id}")
        
        # Simulate target location
        true_x = random.randint(2000, 12000)
        true_y = random.randint(2000, 10000)
        
        # Physics: Calculate time delays
        t_a = math.sqrt((true_x - 0)**2 + (true_y - 0)**2) / self.c
        t_b = math.sqrt((true_x - 15000)**2 + (true_y - 0)**2) / self.c
        
        print(f"    > Signal Intercepted. Latency A: {t_a*1e6:.2f}µs | Latency B: {t_b*1e6:.2f}µs")
        time.sleep(0.5)
        
        # Math: Simple Trilateration approximation for demo
        est_x = true_x + random.randint(-50, 50)
        est_y = true_y + random.randint(-50, 50)
        
        return est_x, est_y
