import unittest
import pandas as pd
import utils.extractor as exc


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

        time, time_median, time_average = exc.Extractor.calculate_time(notes)

        self.assertEqual(time_median, 8.5)
        self.assertEqual(time, 344)
        self.assertEqual(int(time_average), 43)

    def test_calculate_section_1(self):
        notes = []
        ser = pd.Series(data={'X': 1, 'Y': 1}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 1, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 5, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 6, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 6, 'Y': 7}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 10, 'Y': 11}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 100, 'Y': 110}, index=['X', 'Y'])
        notes.append(ser)

        (average_section,
         max_section_1,
         max_section_2,
         max_section_3,
         max_section_4,
         max_section_5,
         median_section
         ) = exc.Extractor.calculate_section(notes)

        self.assertEqual(int(max_section_1), 133)
        self.assertEqual(int(max_section_2), 5)
        self.assertEqual(int(max_section_3), 4)
        self.assertEqual(int(max_section_4), 4)
        self.assertEqual(int(max_section_5), 2)

    def test_calculate_section_2(self):
        notes = []
        ser = pd.Series(data={'X': 1, 'Y': 1}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 1, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)
        ser = pd.Series(data={'X': 5, 'Y': 3}, index=['X', 'Y'])
        notes.append(ser)

        (average_section,
         max_section_1,
         max_section_2,
         max_section_3,
         max_section_4,
         max_section_5,
         median_section
         ) = exc.Extractor.calculate_section(notes)

        self.assertEqual(int(max_section_1), 4)
        self.assertEqual(int(max_section_2), 2)
        self.assertEqual(int(max_section_3), 0)
        self.assertEqual(int(max_section_4), 0)
        self.assertEqual(int(max_section_5), 0)

        self.assertEqual(average_section, 3)
        self.assertEqual(median_section, 3)
