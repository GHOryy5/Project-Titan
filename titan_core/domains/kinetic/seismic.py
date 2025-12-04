import numpy as np
import time
import random

class TitanTunnel:
    def __init__(self):
        print("[*] TITAN TUNNEL: SEISMIC ARRAY CONNECTED")
        
    def listen_ground(self):
        """
        Simulates Distributed Acoustic Sensing (DAS).
        We generate a wave, run FFT, and check for the 'Digging' signature (3-5Hz).
        """
        print("[*] Calibrating geophones...")
        time.sleep(1)
        
        # Simulation: 30% chance of detecting a tunnel
        is_threat = random.choice([True, False, False])
        
        if is_threat:
            # Simulate a 4Hz digging signal with high energy
            freq = 4.2
            energy = 85
            depth = random.randint(8, 15)
            signature = "RHYTHMIC_IMPACT (Pickaxe/Drill)"
            threat_level = "CRITICAL"
            color = "\033[1;31m" # Red
        else:
            # Simulate surface traffic (60Hz) or silence
            freq = 60.0
            energy = 20
            depth = 0
            signature = "SURFACE_NOISE (Vehicle)"
            threat_level = "SAFE"
            color = "\033[1;32m" # Green

        print(f"    > FFT Analysis: Peak Freq {freq}Hz | Energy: {energy}dB")
        print(f"    > Classification: {signature}")
        
        if threat_level == "CRITICAL":
            print(f"{color}[!] ANOMALY DETECTED: SUBTERRANEAN MOVEMENT\033[0m")
            print(f"    > Estimated Depth: {depth} meters")
            return True, depth
        else:
            print(f"{color}[+] Ground Status: STABLE\033[0m")
            return False, 0
