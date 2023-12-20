import unittest
import pandas as pd
from data_extraction import calculate_time, calculate_section


class TestUnit(unittest.TestCase):

    def test_calculate_time(self):
        notes = []

        ser = pd.Series(data={'T': 1}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 12}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 13}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 14}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 17}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 23}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 123}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 167}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 345}, index=['T'])
        notes.append(ser)

        time, time_median, time_average = calculate_time(notes)

        self.assertEqual(time_median, 8.5)
        self.assertEqual(time, 344)
        self.assertEqual(int(time_average), 43)

    def test_calculate_section(self):
        notes = []
        ser = pd.Series(data={'X': 1, 'Y': 1}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 1, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 5, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)

        average_section, max_section, median_section = calculate_section(notes)

        self.assertEqual(average_section, 3)
        self.assertEqual(max_section, 4)
        self.assertEqual(median_section, 3)
