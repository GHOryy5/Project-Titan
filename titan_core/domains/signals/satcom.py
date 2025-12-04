import math
import time
import random
from datetime import datetime

class TitanSatcom:
    def __init__(self, db_handle):
        self.db = db_handle
        print("[*] TITAN SATCOM: ORBITAL TRACKING ENGINE LOADED")
        # Simplified TLE (Two-Line Element) Data for active comms satellites
        self.satellites = {
            "IRIDIUM-NEXT (110)": {"inc": 86.4, "alt": 780, "freq": 1626.0},
            "THURAYA-3":          {"inc": 0.0,  "alt": 35786, "freq": 1525.0}, # Geo-stationary
            "INMARSAT-4 F2":      {"inc": 0.0,  "alt": 35786, "freq": 1530.0}
        }
        self.ground_station_lat = 34.55
        self.ground_station_long = 69.11

    def calculate_look_angles(self, sat_alt, sat_lat, sat_long):
        """
        THE MATH: SPHERICAL TRIGONOMETRY
        Calculates Azimuth (Az) and Elevation (El) from Ground to Satellite.
        """
        # Earth Radius
        Re = 6371.0 
        
        # Convert to radians
        lat_s = math.radians(sat_lat)
        lon_s = math.radians(sat_long)
        lat_g = math.radians(self.ground_station_lat)
        lon_g = math.radians(self.ground_station_long)
        
        # Delta Longitude
        d_lon = lon_s - lon_g
        
        # Calculate Elevation (Simplified slant range)
        # In full code, this requires complex vector math (ECI to ECEF frames)
        # For this demo, we simulate a pass based on relative distance
        
        # Mock calculation for display flow
        azimuth = math.degrees(math.atan2(math.sin(d_lon), math.cos(lat_g) * math.tan(lat_s) - math.sin(lat_g) * math.cos(d_lon)))
        if azimuth < 0: azimuth += 360
        
        elevation = random.uniform(10, 85) # Simulating a visible pass
        
        return azimuth, elevation

    def calculate_doppler(self, freq_mhz, relative_velocity_kmps):
        """
        THE PHYSICS: DOPPLER SHIFT
        Delta_F = (Velocity / c) * Frequency
        """
        c = 300000.0 # Speed of light in km/s
        shift_hz = (relative_velocity_kmps / c) * (freq_mhz * 1e6)
        return shift_hz

    def track_pass(self):
        """
        Simulates a 15-second satellite pass overhead.
        """
        print("\n[*] INITIALIZING ORBITAL SCAN...")
        print(f"    > GROUND STATION: {self.ground_station_lat}, {self.ground_station_long}")
        time.sleep(1)

        # Select a random satellite overhead
        target_sat = "IRIDIUM-NEXT (110)"
        sat_data = self.satellites[target_sat]
        
        print(f"[*] ACQUIRING SIGNAL LOCK: {target_sat}")
        print(f"    > ORBIT: LEO (Altitude {sat_data['alt']}km)")
        print(f"    > BASE FREQ: {sat_data['freq']} MHz")
        
        # Simulate the pass
        for i in range(5):
            # Satellite moves across the sky
            az, el = self.calculate_look_angles(sat_data['alt'], self.ground_station_lat + (i*0.1), self.ground_station_long + (i*0.1))
            
            # Physics: Relative velocity changes as it passes overhead (Max at zenith)
            velocity = 7.5 # km/s for LEO
            doppler = self.calculate_doppler(sat_data['freq'], velocity)
            
            # Formatting the output like a real Spectrum Analyzer
            doppler_str = f"+{doppler:.2f}" if doppler > 0 else f"{doppler:.2f}"
            print(f"    [T+{i}s] AZ: {az:.1f}° | EL: {el:.1f}° | DOPPLER: {doppler_str} Hz | SNR: {random.randint(10,30)}dB")
            time.sleep(0.8)

        print("\n[+] PASS COMPLETE. DOWNLINK BUFFER CAPTURED.")
        return True

    def decode_downlink(self, target_id):
        """
        Decodes the intercepted burst.
        """
        print("[*] DEMODULATING QPSK SIGNAL...")
        time.sleep(1)
        print("[*] DECRYPTING GMR-2 CIPHER STREAM...")
        time.sleep(1)
        
        # Intel Logic
        intercept = "Voice Call: 'Move the shipment to the northern cave complex tonight.'"
        print(f"\033[1;32m[+] INTERCEPT SUCCESSFUL:\033[0m")
        print(f"    > CONTENT: {intercept}")
        
        # Save to DB
        self.db.cursor.execute("INSERT INTO loot (target_id, data_type, content, timestamp) VALUES (?, ?, ?, datetime('now'))", 
                              (target_id, "SATCOM_INTERCEPT", intercept))
        self.db.conn.commit()

