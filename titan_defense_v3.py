import numpy as np
import time
import random

# --- THREAT INTELLIGENCE DATABASE (ELINT) ---
THREAT_DATABASE = {
    "ZSU-23-4 SHILKA": {"freq_range": (14000, 16000), "type": "AAA (Gun System)", "danger": "HIGH"},
    "SA-6 GAINFUL":    {"freq_range": (8500, 10500),  "type": "SAM (Missile Radar)", "danger": "EXTREME"},
    "P-18 SPOON REST": {"freq_range": (150, 170),     "type": "Early Warning Radar", "danger": "MEDIUM"}
}

class ElectronicWarfare:
    def __init__(self):
        print("\033[1;33m[*] EW MODULE: PASSIVE RADAR LISTENING ACTIVE...\033[0m")
        
    def scan_spectrum(self, est_y):
        """
        Simulates the RWR (Radar Warning Receiver).
        The SA-6 Gainful has a kill range of ~24km. 
        We simulate detection when entering the outer envelope (Y > 3000m for demo).
        """
        if est_y > 3000:
            # Simulate detecting the Ku-Band Tracking Radar of an SA-6
            # The signal strength gets stronger (frequency lock) as we get closer
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
        self.x = np.matrix([[0], [0], [0], [0]]) 
        
        self.A = np.matrix([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        self.H = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        self.Q = np.eye(4) * std_acc**2
        self.R = np.matrix([[x_std_meas**2, 0], [0, y_std_meas**2]])
        self.P = np.eye(4)

    def predict(self):
        self.x = np.dot(self.A, self.x)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]

    def update(self, z):
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        self.x = self.x + np.dot(K, (z - np.dot(self.H, self.x)))
        I = np.eye(self.A.shape[0]) 
        self.P = (I - np.dot(K, self.H)) * self.P
        return self.x[0:2]

def run_mission():
    print("\033[1;34m[*] TITAN DEFENSE GRID: AIR DEFENSE SIMULATION STARTED\033[0m")
    
    kf = KalmanFilter(dt=0.5, std_acc=0.5, x_std_meas=30.0, y_std_meas=30.0)
    ew_system = ElectronicWarfare()
    
    true_x, true_y = 0, 0
    # SPEED BOOST: 280 m/s (approx 1000 km/h - Fighter Jet Speed)
    vel_x, vel_y = 50, 280 
    
    print(f"{'GRID LOC':<15} {'EW SPECTRUM ANALYSIS':<40} {'C2 ACTION'}")
    print("=" * 80)

    # Run for 30 steps to ensure we cross the 3000m threshold
    for t in range(30):
        true_x += vel_x
        true_y += vel_y
        
        meas_x = true_x + random.gauss(0, 25)
        meas_y = true_y + random.gauss(0, 25)
        
        kf.predict()
        est_pos = kf.update(np.matrix([[meas_x], [meas_y]]))
        
        # --- NUMPY FIX IS HERE ---
        # We use .item() to safely extract the scalar value from the matrix
        est_x = int(est_pos[0].item())
        est_y = int(est_pos[1].item())

        threat, data, freq = ew_system.scan_spectrum(est_y)
        
        loc = f"[{est_x}, {est_y}]"
        
        if threat:
            # ALERT: RED Text
            msg = f"⚠ LOCK-ON: {threat} ({freq} MHz)"
            print(f"{loc:<15} \033[1;31m{msg:<40}\033[0m !!! NO-FLY ZONE !!!")
            
            if data['danger'] == "EXTREME":
                 print(f"               >>> AUTOMATIC COUNTERMEASURES (FLARE/CHAFF) DEPLOYED.")
                 # Break the loop shortly after detection to simulate mission abort
                 if t > 25: 
                     print("\n[*] MISSION ABORTED: HOSTILE AIRSPACE CONFIRMED.")
                     break
        else:
            # CLEAN: Green Text
            msg = "Spectrum Clear..."
            print(f"{loc:<15} \033[1;32m{msg:<40}\033[0m Scanning...")
            
        time.sleep(0.15)

if __name__ == "__main__":
    run_mission()
