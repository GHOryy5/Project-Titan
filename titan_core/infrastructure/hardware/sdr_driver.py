import math
import random
import numpy as np
import time

# Try to import real hardware library, fail gracefully if missing
try:
    from rtlsdr import RtlSdr
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False

class RadioInterface:
    def __init__(self, center_freq=100.0, sample_rate=2.048e6):
        self.center_freq = center_freq * 1e6 # Convert to Hz
        self.sample_rate = sample_rate
        self.gain = 'auto'
        self.sdr = None
        self.mode = "SIMULATION"
        
        if HARDWARE_AVAILABLE:
            try:
                self.sdr = RtlSdr()
                self.sdr.sample_rate = self.sample_rate
                self.sdr.center_freq = self.center_freq
                self.sdr.gain = self.gain
                self.mode = "LIVE_HARDWARE"
                print(f"[HAL] HARDWARE DETECTED: RTL-SDR device initialized at {center_freq}MHz")
            except Exception as e:
                print(f"[HAL] HARDWARE ERROR: {e}. Falling back to SIMULATION.")
        else:
            print(f"[HAL] No SDR Driver found (pyrtlsdr). Running in SIMULATION MODE.")

    def read_power_level(self, freq_mhz):
        """
        Reads raw RF power at a specific frequency.
        """
        target_freq = freq_mhz * 1e6
        
        if self.mode == "LIVE_HARDWARE":
            try:
                self.sdr.center_freq = target_freq
                # Read 1024 samples (complex numbers)
                samples = self.sdr.read_samples(1024)
                # Calculate Power Spectral Density (PSD) approx
                # Power = sum(real^2 + imag^2) / N
                power = np.mean(np.abs(samples)**2)
                # Convert to dBm
                return 10 * np.log10(power)
            except Exception as e:
                print(f"[HAL] READ ERROR: {e}")
                return -100.0
                
        else:
            # SIMULATION MODE: High Fidelity Noise Generator
            # Simulate a noise floor around -100 dBm
            base_noise = -100 + random.gauss(0, 2)
            
            # Simulate 'spikes' if we hit specific trigger freqs
            triggers = [315.0, 433.9, 900.0, 1800.0]
            for t in triggers:
                if abs(freq_mhz - t) < 0.5:
                    # 40% chance of signal presence
                    if random.random() < 0.4:
                        return random.uniform(-60, -40) # Strong Signal
            
            return base_noise

    def close(self):
        if self.sdr:
            self.sdr.close()
