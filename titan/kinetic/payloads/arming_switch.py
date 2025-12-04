import hashlib
import hmac
import time
from typing import Dict

class SafetyInterlock:
    # Hardcoded hashed keys for simulation (In prod these are in HSM)
    # Key 1: "ALPHA_ONE"
    CMD_KEY_HASH = "5d41402abc4b2a76b9719d911017c592" 
    # Key 2: "BRAVO_TWO"
    XO_KEY_HASH = "7d793037a076dd966144957b34522399"
    
    def __init__(self):
        self.state = "SAFE"
        self.auth_window = 0

    def verify_keys(self, key_a: str, key_b: str) -> bool:
        hash_a = hashlib.md5(key_a.encode()).hexdigest()
        hash_b = hashlib.md5(key_b.encode()).hexdigest()
        
        if hash_a == self.CMD_KEY_HASH and hash_b == self.XO_KEY_HASH:
            self.state = "ARMED"
            self.auth_window = time.time() + 30 # 30 second window to fire
            return True
        return False

    def generate_launch_token(self, target_id: str) -> Dict:
        if self.state != "ARMED":
            raise PermissionError("INTERLOCK LOCKED. DUAL KEYS REQUIRED.")
        
        if time.time() > self.auth_window:
            self.state = "SAFE"
            raise TimeoutError("AUTH WINDOW EXPIRED. RE-KEY REQUIRED.")

        # Generate HMAC-SHA256 Strike Signature
        payload = f"{target_id}:{int(time.time())}"
        signature = hmac.new(
            b'TOP_SECRET_INTERNAL_KEY', 
            payload.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        self.state = "SAFE" # Reset immediately after token generation
        
        return {
            "status": "AUTHORIZED",
            "target": target_id,
            "token": signature,
            "timestamp": time.time()
        }
