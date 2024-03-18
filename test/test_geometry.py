import unittest
import math

from utils.geometry_operations import (
    get_dist,
    get_dist_point_line,
    get_angle_between_vector,
)


class TestUnit(unittest.TestCase):

    def test_geometry(self):
        dist = get_dist_point_line(4, 4, 0, 0, 8, 0)
        self.assertEqual(4, dist)

    def test_geometry_1(self):
        dist = get_dist_point_line(2, 2, 0, 2, 2, 0)
        self.assertAlmostEqual(math.sqrt(2), dist)

    def test_geometry_2(self):
        dist = get_dist_point_line(4, 0, 0, 2, 2, 0)
        self.assertAlmostEqual(math.sqrt(2), dist)

    def test_geometry_3(self):
        dist = get_dist_point_line(6, -2, 0, 2, 2, 0)
        self.assertAlmostEqual(math.sqrt(2), dist)

    def test_geometry_4(self):
        dist = get_dist_point_line(0, 0, 0, 0, 8, 0)
        self.assertAlmostEqual(0, dist)

    def test_geometry_5(self):
        dist = get_dist_point_line(8, 0, 0, 0, 8, 0)
        self.assertAlmostEqual(0, dist)
