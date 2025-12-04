import numpy as np
import time
import random

# --- THREAT INTELLIGENCE DATABASE (ELINT) ---
# We map intercepted frequencies to known Russian/Soviet Air Defense Systems.
THREAT_DATABASE = {
    "ZSU-23-4 SHILKA": {"freq_range": (14000, 16000), "type": "AAA (Gun System)", "danger": "HIGH"},
    "SA-6 GAINFUL":    {"freq_range": (8500, 10500),  "type": "SAM (Missile Radar)", "danger": "EXTREME"},
    "P-18 SPOON REST": {"freq_range": (150, 170),     "type": "Early Warning Radar", "danger": "MEDIUM"}
}

class ElectronicWarfare:
    def __init__(self):
        print("\033[1;33m[*] EW MODULE: LISTENING FOR RADAR EMISSIONS...\033[0m")
        
    def scan_spectrum(self, est_y):
        """
        Simulates the RWR (Radar Warning Receiver).
        If the target moves North (Y > 4000), it enters the kill range of an SA-6 battery.
        """
        if est_y > 4000:
            # Simulate detecting the Ku-Band Tracking Radar of an SA-6
            detected_freq = random.randint(9000, 9500) 
            
            # Match frequency against database
            for name, data in THREAT_DATABASE.items():
                low, high = data['freq_range']
                if low <= detected_freq <= high:
                    return name, data, detected_freq
        return None, None, 0

class KalmanFilter:
    def __init__(self, dt, std_acc, x_std_meas, y_std_meas):
        self.dt = dt
        # State Vector: [x, y, vx, vy] (4x1 Matrix)
        self.x = np.matrix([[0], [0], [0], [0]]) 
        
        # State Transition Matrix (Physics: pos = pos + vel*time)
        self.A = np.matrix([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Measurement Matrix (We measure x, y) -> Maps 4 states to 2 measurements
        self.H = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        # Noise Covariance Matrices
        self.Q = np.eye(4) * std_acc**2
        self.R = np.matrix([[x_std_meas**2, 0], [0, y_std_meas**2]])
        self.P = np.eye(4) # Initial Uncertainty

    def predict(self):
        self.x = np.dot(self.A, self.x)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]

    def update(self, z):
        # 1. Calculate Kalman Gain
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        
        # 2. Update State Estimate
        self.x = self.x + np.dot(K, (z - np.dot(self.H, self.x)))
        
        # 3. Update Uncertainty (Covariance)
        # FIX: Identity matrix I must match the STATE size (4x4), not measurement size (2x2)
        I = np.eye(self.A.shape[0]) 
        self.P = (I - np.dot(K, self.H)) * self.P
        
        return self.x[0:2]

def run_mission():
    print("\033[1;34m[*] TITAN DEFENSE GRID: TRACKING & EW ONLINE\033[0m")
    
    # Init Filter: dt=0.1s, High measurement noise (20m)
    kf = KalmanFilter(dt=0.1, std_acc=0.1, x_std_meas=20.0, y_std_meas=20.0)
    ew_system = ElectronicWarfare()
    
    true_x, true_y = 0, 0
    vel_x, vel_y = 20, 35 # Target is moving fast North-East
    
    print(f"{'GRID LOC':<15} {'EW SPECTRUM ANALYSIS':<40} {'C2 ACTION'}")
    print("=" * 75)

    for t in range(25):
        # 1. Move the Target (Simulation)
        true_x += vel_x
        true_y += vel_y
        
        # 2. Add Measurement Noise (Radio Interference)
        meas_x = true_x + random.gauss(0, 20)
        meas_y = true_y + random.gauss(0, 20)
        
        # 3. Kalman Filter: Clean the signal
        kf.predict()
        est_pos = kf.update(np.matrix([[meas_x], [meas_y]]))
        
        est_x = int(float(est_pos[0]))
        est_y = int(float(est_pos[1]))

        # 4. EW Check: Do we hear any SAM Radar?
        threat, data, freq = ew_system.scan_spectrum(est_y)
        
        # 5. Output to Command & Control
        loc = f"[{est_x}, {est_y}]"
        
        if threat:
            # ALERT: RED Text for SAM Detection
            msg = f"⚠ RADAR LOCK: {threat} ({freq} MHz)"
            print(f"{loc:<15} \033[1;31m{msg:<40}\033[0m !!! NO-FLY ZONE !!!")
            
            if data['danger'] == "EXTREME":
                 print(f"               >>> AUTOMATIC FLIGHT ABORT SIGNAL SENT.")
        else:
            # CLEAN: Green Text
            msg = "Spectrum Clear..."
            print(f"{loc:<15} \033[1;32m{msg:<40}\033[0m Tracking...")
            
        time.sleep(0.2)

if __name__ == "__main__":
    run_mission()
