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

        (time,
         time_max1,
         time_max2,
         time_max3,
         time_max4,
         time_max5,
         time_median,
         time_average,
         ) = exc.Extractor.calculate_time(notes)

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

        (max_section_1,
         max_section_2,
         max_section_3,
         max_section_4,
         max_section_5,
         median_section,
         average_section,
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

        (max_section_1,
         max_section_2,
         max_section_3,
         max_section_4,
         max_section_5,
         median_section,
         average_section,
         ) = exc.Extractor.calculate_section(notes)

        self.assertEqual(int(max_section_1), 4)
        self.assertEqual(int(max_section_2), 2)
        self.assertEqual(int(max_section_3), 0)
        self.assertEqual(int(max_section_4), 0)
        self.assertEqual(int(max_section_5), 0)

        self.assertEqual(average_section, 3)
        self.assertEqual(median_section, 3)

    def test_time_1(self):
        notes = []
        ser = pd.Series(data={'T': 1}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 3}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 12}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 1222}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 12222}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 12234}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 12345}, index=['T'])
        notes.append(ser)

        (time,
         time_max1,
         time_max2,
         time_max3,
         time_max4,
         time_max5,
         time_median,
         time_average,
         ) = exc.Extractor.calculate_time(notes)

        self.assertEqual(int(time_max1), 11000)
        self.assertEqual(int(time_max2), 1210)
        self.assertEqual(int(time_max3), 111)
        self.assertEqual(int(time_max4), 12)
        self.assertEqual(int(time_max5), 9)

    def test_time_2(self):
        notes = []
        ser = pd.Series(data={'T': 1}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 3}, index=['T'])
        notes.append(ser)
        ser = pd.Series(data={'T': 5}, index=['T'])
        notes.append(ser)

        (time,
         time_max1,
         time_max2,
         time_max3,
         time_max4,
         time_max5,
         time_median,
         time_average,
         ) = exc.Extractor.calculate_time(notes)

        self.assertEqual(int(time_max1), 2)
        self.assertEqual(int(time_max2), 2)
        self.assertEqual(int(time_max3), 0)
        self.assertEqual(int(time_max4), 0)
        self.assertEqual(int(time_max5), 0)

        self.assertEqual(int(time_median), 2)
        self.assertEqual(int(time_average), 2)
        self.assertEqual(time, 4)
