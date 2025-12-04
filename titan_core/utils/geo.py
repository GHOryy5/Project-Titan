import math
from titan_core.config.settings import Config

class GeoMath:
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """
        Industrial strength distance calculation.
        Returns distance in meters.
        """
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        
        a = math.sin(dphi/2)**2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return Config.R_EARTH * c

    @staticmethod
    def bearing(lat1, lon1, lat2, lon2):
        """
        Calculates initial compass bearing.
        """
        y = math.sin(math.radians(lon2-lon1)) * math.cos(math.radians(lat2))
        x = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - \
            math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.cos(math.radians(lon2-lon1))
        
        t = math.atan2(y, x)
        return (math.degrees(t) + 360) % 360
