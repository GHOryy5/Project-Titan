import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SystemConfig:
    # Geodetic Constants (WGS84)
    EARTH_RADIUS_M: float = 6378137.0
    FLATTENING: float = 1 / 298.257223563
    
    # Signal Propagation Constants
    PATH_LOSS_EXPONENT_URBAN: float = 3.0
    PATH_LOSS_EXPONENT_RURAL: float = 2.0
    REFERENCE_FREQ_MHZ: float = 900.0
    NOISE_FLOOR_DBM: float = -120.0
    
    # Kinetic Engagement Rules
    MIN_ENGAGEMENT_ALTITUDE_FT: int = 1500
    MAX_LOITER_TIME_MIN: int = 240
    ROE_LEVEL: str = "WEAPONS_HOLD" 
    
    # Infrastructure
    NEO4J_URI: str = os.getenv("TITAN_GRAPH_URI", "bolt://localhost:7687")
    POSTGRES_URI: str = os.getenv("TITAN_SQL_URI", "postgresql://user:pass@localhost/titan")
    TOR_PROXY: str = "socks5h://127.0.0.1:9050"

    # Cryptography
    MASTER_KEY_PATH: str = "/etc/titan/keys/master.pem"
    AUTH_ROUNDS: int = 100000

class MissionProfile:
    def __init__(self, mission_id: str):
        self.id = mission_id
        self.active_assets: List[str] = []
        self.target_list: Dict[str, float] = {} # Target ID -> Priority Score
        self.comm_channels: List[str] = ["HF", "SATCOM", "4G"]

settings = SystemConfig()
