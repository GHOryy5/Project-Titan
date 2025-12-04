import numpy as np
import time
import random
import math

# --- CONFIGURATION: THREAT LIBRARY (ELINT) ---
# Electronic Intelligence: We look for specific Radar Frequencies (MHz)
# that indicate active Anti-Aircraft systems.
THREAT_DATABASE = {
    "ZSU-23-4 SHILKA": {"freq_range": (14000, 16000), "type": "AAA (Anti-Air Artillery)", "danger": "HIGH"},
    "SA-6 GAINFUL":    {"freq_range": (8000, 10000),  "type": "SAM (Surface-to-Air Missile)", "danger": "EXTREME"},
    "P-18 SPOON REST": {"freq_range": (150, 170),     "type": "Early Warning Radar", "danger": "MEDIUM"}
}

class ElectronicWarfare:
    def __init__(self):
        print("\033[1;33m[*] EW MODULE: LISTENING FOR RADAR EMISSIONS...\033[0m")
        
    def scan_spectrum(self, current_sector_x, current_sector_y):
        """
        Simulates a Radar Warning Receiver (RWR).
        If the target moves into a zone with active radar, we detect the pulse.
        """
        # Logic: If target is > 5km North (y > 5000), they are near a SAM site
        if current_sector_y > 5000:
            # Simulate detecting a raw radio frequency signal
            detected_freq = random.randint(8000, 16500) 
            
            # Compare detected freq against our Threat Library
            for name, data in THREAT_DATABASE.items():
                low, high = data['freq_range']
                if low <= detected_freq <= high:
                    return name, data, detected_freq
        return None, None, 0

class KalmanFilter:
    def __init__(self, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas):
        self.dt = dt
        self.x = np.matrix([[0], [0], [0], [0]]) # State: x, y, vx, vy
        
        # Physics Model (State Transition)
        self.A = np.matrix([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Measurement Mapping
        self.H = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        # Noise Covariance
        self.Q = np.eye(4) * std_acc**2
        self.R = np.matrix([[x_std_meas**2, 0], [0, y_std_meas**2]])
        self.P = np.eye(4)

    def predict(self):
        self.x = np.dot(self.A, self.x)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]

    def update(self, z):
        # BUG FIX: Removed 'round()' inside the matrix math.
        # We perform the math using floats, then round only for display later.
        
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        
        # Update State
        self.x = self.x + np.dot(K, (z - np.dot(self.H, self.x)))
        
        # Update Covariance
        I = np.eye(self.H.shape[0])
        self.P = (I - np.dot(K, self.H)) * self.P
        
        return self.x[0:2]

def run_mission():
    print("\033[1;34m[*] TITAN DEFENSE GRID: TRACKING & EW ONLINE\033[0m")
    
    # 1. Initialize Systems
    kf = KalmanFilter(dt=0.1, u_x=0, u_y=0, std_acc=0.1, x_std_meas=15.0, y_std_meas=15.0)
    ew_system = ElectronicWarfare()
    
    true_x, true_y = 0, 0
    vel_x, vel_y = 15, 25 # High speed movement North-East
    
    print(f"{'LOC (Grid)':<15} {'THREAT ASSESSMENT':<40} {'ACTION'}")
    print("-" * 75)

    for t in range(30):
        # --- PHYSICS SIMULATION ---
        true_x += vel_x
        true_y += vel_y
        
        # Add Noise (The "Fog of War")
        noise_x = random.gauss(0, 20)
        noise_y = random.gauss(0, 20)
        meas_x = true_x + noise_x
        meas_y = true_y + noise_y
        
        # --- KALMAN TRACKING ---
        kf.predict()
        est_pos = kf.update(np.matrix([[meas_x], [meas_y]]))
        
        # Convert matrix to clean integers for display (BUG FIX APPLIED HERE)
        est_x = int(float(est_pos[0]))
        est_y = int(float(est_pos[1]))

        # --- ELECTRONIC WARFARE SCAN ---
        # Check if the estimated location has active Radar Emissions
        threat_name, threat_data, freq = ew_system.scan_spectrum(est_x, est_y)
        
        # --- COMMAND & CONTROL OUTPUT ---
        loc_str = f"[{est_x}, {est_y}]"
        
        if threat_name:
            # THREAT DETECTED
            alert_color = "\033[1;31m" # RED
            status = f"DETECTED: {threat_name} ({freq} MHz)"
            action = "!!! NO-FLY ZONE ESTABLISHED !!!"
        else:
            # ALL CLEAR
            alert_color = "\033[1;32m" # GREEN
            status = "Spectrum Clean"
            action = "Tracking..."

        print(f"{loc_str:<15} {alert_color}{status:<40}\033[0m {action}")
        
        # If High Danger, simulate sending data to HQ
        if threat_name and threat_data['danger'] == "EXTREME":
            print(f"   >>> UPLOADING TO HQ: {threat_data['type']} Found at Grid {est_x}, {est_y}")
            print(f"   >>> ADVISING AIRSTRIKE ABORT.")
            time.sleep(0.5) # Time lag for alert
            
        time.sleep(0.1)

if __name__ == "__main__":
    run_mission()
