import math
from dataclasses import dataclass

@dataclass
class ReleaseVector:
    altitude_m: float
    velocity_ms: float
    pitch_angle_deg: float
    heading_deg: float

@dataclass
class ImpactPoint:
    lat_offset: float
    lon_offset: float
    time_to_impact: float
    velocity_at_impact: float

class KineticPhysics:
    GRAVITY = 9.80665
    DRAG_COEFFICIENT = 0.295 # GBU-12 Config

    @staticmethod
    def compute_solution(vector: ReleaseVector) -> ImpactPoint:
        # 1. Time of Flight (Freefall with vertical velocity component)
        # h = v_y * t + 0.5 * g * t^2
        v_y = vector.velocity_ms * math.sin(math.radians(vector.pitch_angle_deg))
        
        # Solving quadratic equation for t
        # 0.5g*t^2 + v_y*t - h = 0
        a = 0.5 * KineticPhysics.GRAVITY
        b = v_y
        c = -vector.altitude_m
        
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            raise ValueError("Invalid ballistic trajectory")
            
        time_to_impact = (-b + math.sqrt(discriminant)) / (2 * a)
        
        # 2. Horizontal Distance Traveled (d = v_x * t) - Drag
        # Drag reduces distance exponentially over time
        v_x = vector.velocity_ms * math.cos(math.radians(vector.pitch_angle_deg))
        
        # Simplified drag integration
        distance_m = 0.0
        current_v = v_x
        dt = 0.1 # 100ms integration steps
        t = 0.0
        
        while t < time_to_impact:
            drag_force = 0.5 * 1.225 * (current_v**2) * KineticPhysics.DRAG_COEFFICIENT * 0.1 # Area approx
            decel = drag_force / 227.0 # Mass of GBU-12 (kg)
            current_v -= decel * dt
            distance_m += current_v * dt
            t += dt

        # 3. Convert to Geodetic Offset
        # Approx 1 degree lat = 111,000 meters
        lat_offset = (distance_m * math.cos(math.radians(vector.heading_deg))) / 111111
        lon_offset = (distance_m * math.sin(math.radians(vector.heading_deg))) / 111111
        
        return ImpactPoint(
            lat_offset=lat_offset,
            lon_offset=lon_offset,
            time_to_impact=time_to_impact,
            velocity_at_impact=math.sqrt(current_v**2 + (KineticPhysics.GRAVITY * time_to_impact)**2)
        )
