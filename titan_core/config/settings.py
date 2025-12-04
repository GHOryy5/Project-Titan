import os

class Config:
    VERSION = "15.0-ENTERPRISE"
    DB_PATH = "titan_operations.db"
    
    # Physics Constants
    C = 299792458.0  # Speed of Light
    G = 9.80665      # Gravity
    R_EARTH = 6371e3 # Earth Radius
    
    # Security Constants
    MAX_LOGIN_ATTEMPTS = 3
    ENCRYPTION_STANDARD = "AES-256"
    
    # Grid Config
    GRID_REF_LAT = 34.55
    GRID_REF_LONG = 69.11
