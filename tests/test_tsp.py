import unittest
import sys
sys.path.append('..')

from tsp import compute_arrival_time, analyze_arrival_info, smart_trip
from utils import TripStats, TimeWindow, DispatchWindowViolation
from examples import AuthorsExample, ExampleA

@unittest.skip("Skipping for now.")
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

@unittest.skip("Skipping for now.")
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

    def test_BranchF(self):

        time_windows = [TimeWindow(70, 80),
                        TimeWindow(100, 100)]

        travel_times = (10,)

        ts = TripStats(time_windows=time_windows, travel_times=travel_times)

        i = 0

        ts.t_a[i] = 90
        ts.slack_a[i] = 0
        ts.remDrive_a[i] = 1
        ts.remDuty_a[i] = 4

        ts.t_d[i+1] = 100

        ts = analyze_arrival_info(ts, i)

        self.assertEqual(ts.nRests[i], 1)
        self.assertEqual(ts.t_d[i], 80)
        self.assertEqual(ts.tBest[i], 86)
        self.assertEqual(ts.slack_d[i], 4)
        self.assertEqual(ts.remDuty_d[i], 14)
        self.assertEqual(ts.remDrive_d[i], 11)
        self.assertEqual(ts.wait[i], 0)

        self.assertEqual(ts.t_d_shadow[i+1],100)
        self.assertEqual(ts.t_a_shadow[i], 90)

    def test_BranchH(self):

        time_windows = [TimeWindow(70, 81),
                        TimeWindow(100, 100)]

        travel_times = (10,)

        ts = TripStats(time_windows=time_windows, travel_times=travel_times)

        i = 0

        ts.t_a[i] = 90
        ts.slack_a[i] = 0
        ts.remDrive_a[i] = 1
        ts.remDuty_a[i] = 4

        ts.t_d[i+1] = 100

        ts = analyze_arrival_info(ts, i)

        self.assertEqual(ts.nRests[i], 1)
        self.assertEqual(ts.t_d[i], 80)
        self.assertEqual(ts.tBest[i], 86)
        self.assertEqual(ts.slack_d[i], 4)
        self.assertEqual(ts.remDuty_d[i], 14)
        self.assertEqual(ts.remDrive_d[i], 11)
        self.assertEqual(ts.wait[i], 0)

        self.assertEqual(ts.t_d_shadow[i+1], 100)
        self.assertEqual(ts.t_a_shadow[i], 90)


    def test_BranchG(self):

        time_windows = [TimeWindow(81, 81),
                        TimeWindow(100, 100)]

        travel_times = (10,)

        ts = TripStats(time_windows=time_windows, travel_times=travel_times)

        i = 0

        ts.t_a[i] = 90
        ts.slack_a[i] = 0
        ts.remDrive_a[i] = 1
        ts.remDuty_a[i] = 4

        ts.t_d[i+1] = 100

        with self.assertRaises(DispatchWindowViolation):
            _ = analyze_arrival_info(ts, i)

class TestSmartTrip(unittest.TestCase):

    def test_example_a(self):

        time_windows = ExampleA.WINDOWS
        travel_times = ExampleA.travel_times

        ts = TripStats(time_windows=time_windows, travel_times=travel_times)

        t_a = [100, 90, 61, 60, 40, 11]
        remDrive_a = [float(), 1, 2, 1, 1, 2]
        remDuty_a = [float(), 4, 5, 4, 4, 5]
        slack_a = [0]*6
        tBest = [float(), 86, 0, 56, 36, float()]

        t_d = [100, 70, 61, 50, 20, 11]
        slack_d = [0]*6
        remDrive_d = [11, 11, 2, 11, 11, 2]
        remDuty_d = [14, 14, 5, 14, 14, 5]
        wait = [0]*6
        rests = [0, 2, 0, 1, 2, float()]

        status, ts = smart_trip(ts)

        self.assertTrue(status)

        for i, expected_value in enumerate(reversed(t_a)):

            with self.subTest(variable="t_a", i=i):
                self.assertEqual(expected_value, ts.t_a[i])

        for i, expected_value in enumerate(reversed(slack_a)):

            with self.subTest(variable="slack_a", i=i):
                self.assertEqual(expected_value, ts.slack_a[i])

        for i, expected_value in enumerate(reversed(remDrive_a)):

            with self.subTest(variable="remDrive_a", i=i):
                self.assertEqual(expected_value, ts.remDrive_a[i])

        for i, expected_value in enumerate(reversed(remDuty_a)):

            with self.subTest(variable="remDuty_a", i=i):
                self.assertEqual(expected_value, ts.remDuty_a[i])

        for i, expected_value in enumerate(reversed(tBest)):

            with self.subTest(variable="tBest", i=i):
                self.assertEqual(expected_value, ts.tBest[i])

        for i, expected_value in enumerate(reversed(t_d)):

            with self.subTest(variable="t_d", i=i):
                self.assertEqual(expected_value, ts.t_d[i])

        for i, expected_value in enumerate(reversed(slack_d)):

            with self.subTest(variable="slack_d", i=i):
                self.assertEqual(expected_value, ts.slack_d[i])

        for i, expected_value in enumerate(reversed(remDrive_d)):

            with self.subTest(variable="remDrive_d", i=i):
                self.assertEqual(expected_value, ts.remDrive_d[i])

        for i, expected_value in enumerate(reversed(remDuty_d)):

            with self.subTest(variable="remDuty_d", i=i):
                self.assertEqual(expected_value, ts.remDuty_d[i])

        for i, expected_value in enumerate(reversed(wait)):

            with self.subTest(variable="wait", i=i):
                self.assertEqual(expected_value, ts.wait[i])

        for i, expected_value in enumerate(reversed(rests)):

            with self.subTest(variable="rests_between", i=i):
                self.assertEqual(expected_value, ts.nRests[i])


if __name__ == '__main__':
    unittest.main()