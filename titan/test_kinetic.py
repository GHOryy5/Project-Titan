from titan.kinetic.drone_fleet.mavlink import MavLinkBridge
from titan.kinetic.ballistics.impact_calc import KineticPhysics, ReleaseVector
from titan.kinetic.payloads.arming_switch import SafetyInterlock

def run_simulation():
    print("[*] TITAN KINETIC SYSTEMS INITIALIZING...")
    
    # 1. Calculate Ballistics
    vector = ReleaseVector(altitude_m=5000, velocity_ms=200, pitch_angle_deg=-10, heading_deg=90)
    impact = KineticPhysics.compute_solution(vector)
    print(f"[MATH] Impact Calculation: {impact.time_to_impact:.2f}s to target. Offset: {impact.lat_offset:.6f}, {impact.lon_offset:.6f}")
    
    # 2. Generate MAVLink Control Packets
    bridge = MavLinkBridge()
    packet = bridge.pack_vector(34.51, 69.11, 5000, 200)
    bridge.transmit(packet, "192.168.1.50", 14550)
    
    # 3. Attempt Arming
    safety = SafetyInterlock()
    try:
        print("[SEC] Attempting Arm with Single Key...")
        safety.verify_keys("ALPHA_ONE", "WRONG_KEY")
        safety.generate_launch_token("TARGET-A1")
    except Exception as e:
        print(f"[SEC] Safety Interlock Active: {e}")
        
    print("[SEC] Authenticating Dual Keys...")
    if safety.verify_keys("ALPHA_ONE", "BRAVO_TWO"):
        token = safety.generate_launch_token("TARGET-A1")
        print(f"[SEC] LAUNCH AUTHORIZED. TOKEN: {token['token'][:16]}...")

if __name__ == "__main__":
    run_simulation()
