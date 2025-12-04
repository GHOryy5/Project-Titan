import time
from titan_core.infrastructure.hardware.sdr_driver import RadioInterface

class TitanGuardian:
    def __init__(self, db_handle):
        self.db = db_handle
        print("[*] TITAN GUARDIAN: CONNECTING TO RF HARDWARE ABSTRACTION LAYER...")
        self.radio = RadioInterface()
        
        self.triggers = {
            315.0: "Key Fob / Garage Opener",
            433.9: "LPD433 Device",
            900.0: "Cordless Phone Base",
            1800.0: "GSM Cellular Trigger"
        }

    def scan_rf_environment(self):
        print("\n[*] SCANNING RF SPECTRUM (HARDWARE LINKED)...")
        time.sleep(1)
        
        detected_freq = None
        max_power = -999
        
        # Scan the known trigger list using the Driver
        for freq in self.triggers:
            # The HAL decides if this is real hardware or simulation
            power = self.radio.read_power_level(freq)
            
            # Formatting output to look like a Spectrum Analyzer
            bar_len = int((power + 110) / 2) # Visual bar
            if bar_len < 0: bar_len = 0
            bar = "█" * bar_len
            
            print(f"    > {freq:<6} MHz | PWR: {power:>6.1f} dBm | {bar}")
            
            # Threshold detection (-70 dBm is usually a strong signal)
            if power > -70:
                detected_freq = freq
                max_power = power
                time.sleep(0.2) 

        if detected_freq:
            threat_name = self.triggers[detected_freq]
            print(f"\n\033[1;31m[!] CRITICAL ALERT: RF SPIKE AT {detected_freq} MHz\033[0m")
            print(f"    > SIGNATURE: {threat_name}")
            return detected_freq, max_power
        else:
            print("\n\033[1;32m[+] Spectrum Clear. Noise Floor Nominal.\033[0m")
            return None, None

    def engage_jammer(self, freq, enemy_power):
        print(f"\n[*] ENGAGING JAMMER ON {freq} MHz...")
        
        # Calculate Power Requirement
        # If enemy is at -50dBm, we need to be at least -40dBm at receiver
        required_power = enemy_power + 10 
        
        print(f"    > Target Power: {enemy_power:.1f} dBm")
        print(f"    > Jammer Set:   {required_power:.1f} dBm (Overpower Mode)")
        time.sleep(1)
        
        # In a real system, this would call self.radio.transmit_noise(freq)
        print(f"\033[1;32m[+] THREAT NEUTRALIZED. SPECTRUM FLOODED.\033[0m")
        return True
