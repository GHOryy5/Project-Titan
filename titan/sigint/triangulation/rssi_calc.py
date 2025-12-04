import math
from titan.core.config import settings

class SignalPhysics:
    
    @staticmethod
    def calculate_distance_fspl(rssi: float, tx_power: float, freq_mhz: float) -> float:
        """
        Calculate distance using Free Space Path Loss model.
        d = 10 ^ ((TxPower - RSSI - 20log10(f) + 27.55) / 20)
        """
        if rssi > tx_power:
            return 0.0
            
        try:
            # Constant 27.55 is for MHz and Meters
            path_loss = tx_power - rssi
            freq_term = 20 * math.log10(freq_mhz)
            exponent = (path_loss - freq_term + 27.55) / 20.0
            return math.pow(10, exponent)
        except ValueError:
            return -1.0

    @staticmethod
    def calculate_distance_hata(rssi: float, height_tx: float, height_rx: float, freq: float) -> float:
        """
        Okumura-Hata Model for Urban Areas (More accurate for cities).
        L = 69.55 + 26.16log(f) - 13.82log(ht) - a(hr) + (44.9 - 6.55log(ht))log(d)
        """
        # Correction factor for small/medium city
        a_hr = (1.1 * math.log10(freq) - 0.7) * height_rx - (1.56 * math.log10(freq) - 0.8)
        
        # We need to inverse the Hata equation to find 'd' (distance) from 'L' (path loss)
        path_loss = settings.TX_POWER_DEFAULT - rssi # Assuming standard macrocell power
        
        term1 = 69.55 + 26.16 * math.log10(freq)
        term2 = 13.82 * math.log10(height_tx)
        term3 = a_hr
        factor = 44.9 - 6.55 * math.log10(height_tx)
        
        log_d = (path_loss - term1 + term2 + term3) / factor
        return math.pow(10, log_d)

    @staticmethod
    def estimate_position_error(rssi_std_dev: float) -> float:
        """
        Estimates the geolocation error radius based on signal variance (Cramer-Rao Bound approximation).
        """
        return math.exp(rssi_std_dev / 10.0) * 15.0 
