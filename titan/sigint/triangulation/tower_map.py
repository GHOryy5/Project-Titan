import numpy as np
from typing import List, Tuple, Dict
from .rssi_calc import SignalPhysics

class TowerGrid:
    def __init__(self):
        self.towers: Dict[str, Tuple[float, float]] = {} # ID -> (Lat, Lon)
        
    def register_tower(self, tower_id: str, lat: float, lon: float):
        self.towers[tower_id] = (lat, lon)

    def trilaterate_target(self, signal_data: List[Dict]) -> Tuple[float, float]:
        """
        Solves for target (x, y) using Non-Linear Least Squares.
        signal_data: List of {'tower_id': str, 'rssi': float}
        """
        if len(signal_data) < 3:
            raise ValueError("Insufficient signal sources for triangulation (min 3 required)")

        # Convert Lat/Lon to local Cartesian grid for calculation (simplified projection)
        # Origin is the first tower
        origin_id = signal_data[0]['tower_id']
        origin_lat, origin_lon = self.towers[origin_id]
        
        P = [] # Tower coordinates (x, y)
        r = [] # Distances (radii)
        
        for reading in signal_data:
            tid = reading['tower_id']
            t_lat, t_lon = self.towers[tid]
            
            # Equirectangular approximation for local grid (valid for <100km)
            x = (t_lon - origin_lon) * 111320 * np.cos(np.deg2rad(origin_lat))
            y = (t_lat - origin_lat) * 110574
            dist = SignalPhysics.calculate_distance_fspl(reading['rssi'], 46.0, 900.0) # 46dBm = 40W
            
            P.append([x, y])
            r.append(dist)
            
        P = np.array(P)
        r = np.array(r)
        
        # Linearizing the equations for Ax = b
        # 2x(xi - x1) + 2y(yi - y1) = r1^2 - ri^2 + xi^2 + yi^2 - x1^2 - y1^2
        
        A = []
        b = []
        
        x1, y1 = P[0]
        r1 = r[0]
        
        for i in range(1, len(P)):
            xi, yi = P[i]
            ri = r[i]
            
            A.append([2 * (xi - x1), 2 * (yi - y1)])
            b.append(r1**2 - ri**2 + xi**2 + yi**2 - x1**2 - y1**2)
            
        A = np.array(A)
        b = np.array(b)
        
        # Solve Ax = b using Pseudo-Inverse
        target_local = np.linalg.pinv(A).dot(b)
        
        # Convert local (x, y) back to Global Lat/Lon
        tx, ty = target_local
        
        target_lat = origin_lat + (ty / 110574)
        target_lon = origin_lon + (tx / (111320 * np.cos(np.deg2rad(origin_lat))))
        
        return (target_lat, target_lon)
