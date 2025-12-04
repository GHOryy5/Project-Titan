import numpy as np
import time
import random

class KalmanFilter:
    def __init__(self, dt, u_x, u_y, std_acc, x_std_meas, y_std_meas):
        """
        Initializes the Kalman Filter variables.
        dt: sampling time (time for 1 cycle)
        u_x, u_y: acceleration magnitude
        std_acc: process noise magnitude
        x_std_meas, y_std_meas: standard deviation of the measurement
        """
        # Define sampling time
        self.dt = dt

        # Define the State Matrix (X, Y, Velocity_X, Velocity_Y)
        self.x = np.matrix([[0], [0], [0], [0]])

        # Define the State Transition Matrix (A)
        # This represents the physics: New Pos = Old Pos + (Velocity * Time)
        self.A = np.matrix([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Define the Control Input Matrix (B)
        self.B = np.matrix([
            [(self.dt**2)/2, 0],
            [0, (self.dt**2)/2],
            [self.dt, 0],
            [0, self.dt]
        ])

        # Define Measurement Mapping Matrix (H)
        # We only measure Position (X, Y), not Velocity.
        self.H = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        # Initial Process Noise Covariance (Q)
        self.Q = np.matrix([
            [(self.dt**4)/4, 0, (self.dt**3)/2, 0],
            [0, (self.dt**4)/4, 0, (self.dt**3)/2],
            [(self.dt**3)/2, 0, self.dt**2, 0],
            [0, (self.dt**3)/2, 0, self.dt**2]
        ]) * std_acc**2

        # Initial Measurement Noise Covariance (R)
        self.R = np.matrix([
            [x_std_meas**2, 0],
            [0, y_std_meas**2]
        ])

        # Initial Error Covariance (P)
        self.P = np.eye(self.A.shape[1])

    def predict(self):
        # 1. Extrapolate the state
        # x_k = A * x_k-1 + B * u_k
        self.x = np.dot(self.A, self.x) 
        
        # 2. Extrapolate the uncertainty (covariance)
        # P_k = A * P_k-1 * A_T + Q
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x[0:2]

    def update(self, z):
        # z is the raw measurement from TDoA
        
        # 1. Compute Kalman Gain (K)
        # K = P * H_T * inv(H * P * H_T + R)
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # 2. Update estimate with measurement z
        # x = x + K * (z - H * x)
        self.x = round(self.x + np.dot(K, (z - np.dot(self.H, self.x))))

        # 3. Update the error covariance
        # P = (I - K * H) * P
        I = np.eye(self.H.shape[0])
        self.P = (I - np.dot(K, self.H)) * self.P
        
        return self.x[0:2]

def run_simulation():
    print("\033[1;34m[*] TITAN DYNAMIC TRACKING (KALMAN) INITIALIZED\033[0m")
    
    # Initialize Filter
    # dt=0.1s, acceleration=0, noise_acc=0.1, measurement_error=20 meters
    kf = KalmanFilter(0.1, 0, 0, 0.1, 20.0, 20.0)
    
    # Ground Truth: The target starts at (0,0) and drives North-East
    true_x = 0
    true_y = 0
    velocity_x = 15 # m/s (approx 54 km/h)
    velocity_y = 10 
    
    print(f"{'STEP':<6} {'RAW MEASURE (Noisy)':<25} {'KALMAN PREDICTION (Clean)':<25} {'ERROR'}")
    print("-" * 70)

    for t in range(20):
        # 1. Move the Target (Physics)
        true_x += velocity_x
        true_y += velocity_y
        
        # 2. Simulate TDoA Measurement Noise (The "Fog of War")
        # Radio signals bounce, causing jitter (Gaussian Noise)
        noise_x = random.gauss(0, 25) # +/- 25 meters error
        noise_y = random.gauss(0, 25)
        
        measured_x = true_x + noise_x
        measured_y = true_y + noise_y
        
        # 3. Apply Kalman Filter
        kf.predict()
        estimated_pos = kf.update(np.matrix([[measured_x], [measured_y]]))
        est_x = float(estimated_pos[0])
        est_y = float(estimated_pos[1])
        
        # 4. Compare
        # How far off was the raw data vs the Kalman fix?
        raw_error = np.sqrt((true_x - measured_x)**2 + (true_y - measured_y)**2)
        kalman_error = np.sqrt((true_x - est_x)**2 + (true_y - est_y)**2)
        
        color = "\033[1;32m" if kalman_error < raw_error else "\033[1;31m"
        
        print(f"T+{t:<5} "
              f"X:{int(measured_x):<5} Y:{int(measured_y):<5} | "
              f"{color}X:{int(est_x):<5} Y:{int(est_y):<5}\033[0m | "
              f"Raw:{int(raw_error)}m -> Fix:{int(kalman_error)}m")
        
        time.sleep(0.2)

if __name__ == "__main__":
    run_simulation()
