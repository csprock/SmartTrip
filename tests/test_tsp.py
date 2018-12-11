import unittest
import sys
sys.path.append('..')

from tsp import compute_arrival_time, analyze_arrival_info
from utils import TripStats, TimeWindow
from examples import AuthorsExample

class TestComputeArrivalTime(unittest.TestCase):

    @classmethod
    def setUp(self):

        self.ts = TripStats(AuthorsExample.WINDOWS, AuthorsExample.travel_times)

    def test_insufficient_drive_time(self):

        i = 5

        ts = compute_arrival_time(self.ts, i)

        self.assertEqual(ts.nRests_between[i], 1)
        self.assertEqual(ts.t_a[i], 75)
        self.assertEqual(ts.slack_a[i], 28)
        self.assertEqual(ts.remDuty_a[i], 10)
        self.assertEqual(ts.remDrive_a[i], 7)

    def test_sufficient_drive_time(self):

        i = 2

        self.ts.t_d[i+1] = 25
        self.ts.slack_d[i+1] = 0
        self.ts.remDrive_d[i+1] = 5
        self.ts.remDuty_d[i+1] = 8
        self.ts.wait[i+1] = 0
        self.ts.nRests[i+1] = 0

        ts = compute_arrival_time(self.ts, i)

        self.assertEqual(ts.nRests_between[i], 0)
        self.assertEqual(ts.t_a[i], 21)
        self.assertEqual(ts.slack_a[i], 0)
        self.assertEqual(ts.remDuty_a[i], 4)
        self.assertEqual(ts.remDrive_a[i], 1)

class TestAnalyzeArrivalInfo(unittest.TestCase):


    def test_BranchB(self):

        ts = TripStats(AuthorsExample.WINDOWS, AuthorsExample.travel_times)

        i = 1

        ts.t_a[i] = 6
        ts.slack_a[i] = 0
        ts.remDrive_a[i] = 10
        ts.remDuty_a[i] = 13

        ts = analyze_arrival_info(ts, i)

        self.assertEqual(ts.nRests[i], 0)
        self.assertEqual(ts.t_d[i], 6)
        self.assertEqual(ts.tBest[i], 0)
        self.assertEqual(ts.slack_d[i], 0)
        self.assertEqual(ts.remDuty_d[i], 13)
        self.assertEqual(ts.remDrive_d[i], 10)
        self.assertEqual(ts.wait[i], 0)

    def test_BranchC(self):

        ts = TripStats(AuthorsExample.WINDOWS, AuthorsExample.travel_times)

        i = 2

        ts.t_a[i] = 21
        ts.slack_a[i] = 0
        ts.remDrive_a[i] = 1
        ts.remDuty_a[i] = 4

        ts.t_d[i+1] = 25

        ts = analyze_arrival_info(ts, i)

        self.assertEqual(ts.nRests[i], 0)
        self.assertEqual(ts.t_d[i], 18)
        self.assertEqual(ts.tBest[i], 17)
        self.assertEqual(ts.slack_d[i], 0)
        self.assertEqual(ts.remDuty_d[i], 1)
        self.assertEqual(ts.remDrive_d[i], 1)
        self.assertEqual(ts.wait[i], 3)

        self.assertEqual(ts.t_d_shadow[i+1], 25)
        self.assertEqual(ts.t_a_shadow[i], 21)

    def test_BranchE(self):

        time_windows = [TimeWindow(10, 20),
                        TimeWindow(100, 100)]

        travel_times = (10,)

        ts = TripStats(time_windows=time_windows, travel_times=travel_times)

        ts.t_a[0] = 90
        ts.slack_a[0] = 0
        ts.remDrive_a[0] = 1
        ts.remDuty_a[0] = 4

        ts = analyze_arrival_info(ts, 0)

        self.assertEqual(ts.nRests[0], 3)
        self.assertEqual(ts.t_d[0], 20)
        self.assertEqual(ts.tBest[0], 86)
        self.assertEqual(ts.slack_d[0], 0)
        self.assertEqual(ts.remDuty_d[0], 6)
        self.assertEqual(ts.remDrive_d[0], 6)
        self.assertEqual(ts.wait[0], 40)





if __name__ == '__main__':
    unittest.main()