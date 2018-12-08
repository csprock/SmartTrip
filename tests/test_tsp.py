import unittest
import sys
sys.path.append('..')

from tsp import compute_arrival_time
from utils import TripStats, TimeWindow
from examples import AuthorsExample

class TestComputeArrivalTime(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.ts = TripStats(AuthorsExample.WINDOWS, AuthorsExample.travel_times)


    def test_sufficient_drive_time(self):

        i = 5

        ts = compute_arrival_time(self.ts, i)

        self.assertEqual(ts.nRests_between[i], 1)
        self.assertEqual(ts.t_a[i], 75)
        self.assertEqual(ts.slack_a[i], 28)
        self.assertEqual(ts.remDuty_a[i], 10)
        self.assertEqual(ts.remDrive_a[i], 7)

if __name__ == '__main__':
    unittest.main()