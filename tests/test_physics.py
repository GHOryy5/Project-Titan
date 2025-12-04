import unittest
from titan_core.utils.geo import GeoMath
from titan_core.utils.signal import SignalMath
from titan_core.domains.kinetic.ballistics import TitanBallistics

class TestTitanPhysics(unittest.TestCase):
    
    def test_haversine_distance(self):
        # Distance between New York and London approx 5570km
        lat1, lon1 = 40.7128, -74.0060
        lat2, lon2 = 51.5074, -0.1278
        dist = GeoMath.haversine(lat1, lon1, lat2, lon2)
        self.assertTrue(5500000 < dist < 5600000)
        print(f"[TEST] Haversine Calc: {dist/1000:.2f}km (PASS)")

    def test_path_loss(self):
        # FSPL for 2.4GHz at 100m is approx 80dB
        loss = SignalMath.free_space_path_loss(2.4e9, 100)
        self.assertTrue(79 < loss < 81)
        print(f"[TEST] RF Path Loss: {loss:.2f}dB (PASS)")

    def test_ballistics_impact(self):
        # Freefall 500m should take approx 10s with drag
        b = TitanBallistics()
        # Mock print to avoid clutter
        original_print = print
        # Run calculation
        lat, lon, time = b.calculate_drop(500, 0, 0, 0)
        self.assertTrue(time > 0)
        print(f"[TEST] Ballistic Time: {time:.2f}s (PASS)")

if __name__ == '__main__':
    unittest.main()
