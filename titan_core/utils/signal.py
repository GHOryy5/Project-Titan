import math
from titan_core.config.settings import Config

class SignalMath:
    @staticmethod
    def free_space_path_loss(freq_hz, dist_m):
        """
        FSPL = 20log10(d) + 20log10(f) + 20log10(4pi/c)
        Returns Loss in dB.
        """
        if dist_m <= 0: return 0.0
        return 20 * math.log10(dist_m) + \
               20 * math.log10(freq_hz) - 147.55

    @staticmethod
    def doppler_shift(freq_hz, velocity_mps):
        return (velocity_mps / Config.C) * freq_hz
