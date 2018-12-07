import sys
import unittest
sys.path.append('..')
from utils import construct_trip, drive, wait_no_rest, rest_no_wait, pushed_up_rests_with_wait, rests_with_waits

# TODO: rename test functions and data inputs
# TODO: create helper function for checking lists element-wise
# TODO: create help function to run function with given inputs


class TestDrive(unittest.TestCase):

    '''
    Tests for the drive() function used in trip_constructor().
    '''

    @classmethod
    def setUpClass(cls):

        #### No rests between driving ####
        # No rests between driving, remDrive_d > time remaining to destination
        cls.drive_scenario_1a_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 0,
            't_a': 15,
            'remDrive_d': 6
        }

        # No rests between driving, remDrive_d == time remaining to destination
        cls.drive_scenario_1b_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 0,
            't_a': 15,
            'remDrive_d': 5
        }

        #### Rests between driving ####
        # 1 rest between driving
        cls.drive_scenario_2a_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 1,
            't_a': 0,
            'remDrive_d': 5
        }

        # multiple rests between driving
        cls.drive_scenario_2b_input = {
            'T': 40,
            'legs': [],
            'nRests_between': 2,
            't_a': 0,
            'remDrive_d': 5
        }

        # start driving without any remaining drive time
        cls.drive_scenario_2c_input = {
            'T': 60,
            'legs': [],
            'nRests_between': 3,
            't_a': 0,
            'remDrive_d': 0
        }

        #### Test inadequet rests exceptions ####
        # Remaining drive time less that time remaining to destination
        # but number of rests = 0
        cls.drive_senario_3a_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 0,
            't_a': 10,
            'remDrive_d': 5
        }

        # Not enough rests given to cover required time
        cls.drive_scenario_3b_input = {
            'T': 40,
            'legs': [],
            'nRests_between': 1,
            't_a': 5,
            'remDrive_d': 1
        }


    def test_scenario_1a(self):

        expected = [('drive', 15, 20)]

        T, legs = drive(**self.drive_scenario_1a_input)


        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_1b(self):

        expected = [('drive', 15, 20)]

        T, legs = drive(**self.drive_scenario_1b_input)


        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_2a(self):

        expected = [('drive', 15, 20),
                  ('rest', 5, 15),
                  ('drive', 0, 5)]

        T, legs = drive(**self.drive_scenario_2a_input)

        self.assertEqual(len(legs), 3)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_2b(self):

        expected = [('drive', 35, 40),
                  ('rest', 25, 35),
                  ('drive', 14, 25),
                  ('rest', 4, 14),
                  ('drive', 0, 4)]

        T, legs = drive(**self.drive_scenario_2b_input)

        self.assertEqual(len(legs), 5)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_2c(self):

        expected = [('rest', 50, 60),
                  ('drive', 39, 50),
                  ('rest', 29, 39),
                  ('drive', 18, 29),
                  ('rest', 8, 18),
                  ('drive', 0, 8)]

        T, legs = drive(**self.drive_scenario_2c_input)

        self.assertEqual(len(legs), 6)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_3a(self):

        # TODO: create regex match and use assertRaisesRegex
        with self.assertRaises(ValueError):

            _, _ = drive(**self.drive_senario_3a_input)

    def test_scenario_3b(self):

        # TODO: create regex match and use assertRaisesRegex
        with self.assertRaises(ValueError):

            T, legs = drive(**self.drive_scenario_3b_input)


class TestWaitNoRest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Scenario 1: normal waiting, t_d > t_a and t_d - t_a <= 14
        cls.scenario_1_input = {
            'T': 5,
            'legs': [],
            't_d': 3,
            't_a': 5
        }

        # Check assertion t_d < t_a
        cls.assertion_1_input = {
            'T': 3,
            'legs': [],
            't_d': 5,
            't_a': 3
        }

        # Check assertion that T == t_a
        cls.assertion_2_input = {
            'T': 5,
            'legs': [],
            't_d': 3,
            't_a': 4
        }

        # Check assertion that t_a - t_d <= 14
        cls.assertion_3_input = {
            'T': 15,
            'legs': [],
            't_a': 15,
            't_d': 0
        }


    def test_scenario_1(self):

        expected = [('wait', 3, 5)]

        T, legs = wait_no_rest(**self.scenario_1_input)

        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 3)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = wait_no_rest(**self.assertion_1_input)

    def test_assertion_2(self):

        with self.assertRaises(AssertionError):

            _, _ = wait_no_rest(**self.assertion_2_input)

    def test_assertion_3(self):

        with self.assertRaises(AssertionError):

            _, _ = wait_no_rest(**self.assertion_3_input)


class TestRestNoWait(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.scenario_1 = {
            'T': 20,
            'legs': [],
            'nRests': 2
        }

        cls.assertion_1 = {
            'T': 20,
            'legs': [],
            'nRests': 0
        }


    def test_scenario_1(self):

        expected = [('rest', 10, 20),
                    ('rest', 0, 10)]

        T, legs = rest_no_wait(**self.scenario_1)

        self.assertEqual(len(legs), 2)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])


    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = rest_no_wait(**self.assertion_1)

# TODO: rests_with_waits
class TestRestWithWaits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # TODO: do multi-rest analogs for scenarios 1-3
        # wait > remDuty
        cls.scenario_1_input = {
            'T': 29,
            'legs': [],
            'nRests': 1,
            't_d': 10,
            'remDuty_a': 3,
            'wait': 9
        }
        # wait = remDuty (no wait after rest)
        cls.scenario_2_input = {
            'T': 29,
            'legs': [],
            'nRests': 1,
            't_d': 16,
            'remDuty_a': 3,
            'wait': 3
        }
        # no remaining drive, single rest
        cls.scenario_3_input = {
            'T': 29,
            'legs': [],
            'nRests': 1,
            't_d': 15,
            'remDuty_a': 0,
            'wait': 4
        }
        # remaining rests, multiple rests, wait > remDuty
        cls.scenario_4_input = {
            'T': 90,
            'legs': [],
            'nRests': 2,
            't_d': 44,
            'remDuty_a': 4,
            'wait': 26
        }
        # multiple rests, no remDuty
        cls.scenario_5_input = {
            'T': 90,
            'legs': [],
            'nRests': 2,
            't_d': 54,
            'remDuty_a': 0,
            'wait': 16
        }

        # multiple rests, no remDuty, no wait after last rest
        cls.scenario_6_input = {
            'T': 90,
            'legs': [],
            'nRests': 2,
            't_d': 56,
            'remDuty_a': 0,
            'wait': 14
        }

        # test assertion
        cls.assertion_1 = {
            'T': 29,
            'legs': [],
            'nRests': 1,
            't_d': 14,
            'remDuty_a': 0,
            'wait': 4
        }

    def test_scenario_1(self):

        expected = [('wait', 26, 29),
                    ('rest', 16, 26),
                    ('wait', 10, 16)]

        T, legs = rests_with_waits(**self.scenario_1_input)

        self.assertEqual(len(legs), 3)
        self.assertEqual(T, 10)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_2(self):

        expected = [('wait', 26, 29),
                    ('rest', 16, 26)]

        T, legs = rests_with_waits(**self.scenario_2_input)

        self.assertEqual(len(legs), 2)
        self.assertEqual(T, 16)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_3(self):

        expected = [('rest', 19, 29),
                    ('wait', 15, 19)]

        T, legs = rests_with_waits(**self.scenario_3_input)

        self.assertEqual(len(legs), 2)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_4(self):

        expected = [('wait', 86, 90),
                    ('rest', 76, 86),
                    ('wait', 62, 76),
                    ('rest', 52, 62),
                    ('wait', 44, 52)]

        T, legs = rests_with_waits(**self.scenario_4_input)

        self.assertEqual(len(legs), 5)
        self.assertEqual(T, 44)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_5(self):

        expected = [('rest', 80, 90),
                    ('wait', 66, 80),
                    ('rest', 56, 66),
                    ('wait', 54, 56)]

        T, legs = rests_with_waits(**self.scenario_5_input)

        self.assertEqual(len(legs), 4)
        self.assertEqual(T, 54)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_6(self):

        expected = [('rest', 80, 90),
                    ('wait', 66, 80),
                    ('rest', 56, 66)]

        T, legs = rests_with_waits(**self.scenario_6_input)

        self.assertEqual(len(legs), 3)
        self.assertEqual(T, 56)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])


    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = rests_with_waits(**self.assertion_1)


# TODO: pushed_up_rests_with_wait
class TestPushedUpRestsWithWait(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # resting takes all time between arrival and departure, no waits
        cls.scenario_1 = {
            'T': 60,
            'legs': [],
            'nRests': 2,
            't_d': 40,
            'remDuty_d': 0,
            'wait': 0
        }
        # wait = remDuty_d
        cls.scenario_2 = {
            'T': 40,
            'legs': [],
            'nRests': 2,
            't_d': 15,
            'remDuty_d': 5,
            'wait': 5
        }
        # uses all remDuty, 3 rests with no waiting after
        cls.scenario_3 = {
            'T': 80,
            'legs': [],
            'nRests': 3,
            't_d': 31,
            'remDuty_d': 5,
            'wait': 19
        }
        # uses all remDuty, 3 rests with some waiting after last rest
        cls.scenario_4 = {
            'T': 80,
            'legs': [],
            'nRests': 3,
            't_d': 30,
            'remDuty_d': 5,
            'wait': 20
        }
        # no remDuty but wait after last rest
        cls.scenario_5 = {
            'T': 60,
            'legs': [],
            'nRests': 2,
            't_d': 35,
            'remDuty_d': 0,
            'wait': 5
        }

        # test assertion statement (same as above with one extra hour of wait)
        cls.assertion_1 = {
            'T': 80,
            'legs': [],
            'nRests': 3,
            't_d': 30,
            'remDuty_d': 5,
            'wait': 21
        }

    def test_scenario_1(self):

        expected = [('rest', 50, 60),
                    ('rest', 40, 50)]

        T, legs = pushed_up_rests_with_wait(**self.scenario_1)

        self.assertEqual(T, 40)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_2(self):

        expected = [('wait', 35, 40),
                    ('rest', 25, 35),
                    ('rest', 15, 25)]

        T, legs = pushed_up_rests_with_wait(**self.scenario_2)

        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_3(self):

        expected = [('wait', 75, 80),
                    ('rest', 65, 75),
                    ('wait', 51, 65),
                    ('rest', 41, 51),
                    ('rest', 31, 41)]

        T, legs = pushed_up_rests_with_wait(**self.scenario_3)

        self.assertEqual(T, 31)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_4(self):

        expected = [('wait', 75, 80),
                    ('rest', 65, 75),
                    ('wait', 51, 65),
                    ('rest', 41, 51),
                    ('rest', 31, 41),
                    ('wait', 30, 31)]

        T, legs = pushed_up_rests_with_wait(**self.scenario_4)

        self.assertEqual(T, 30)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_scenario_5(self):

        expected = [('rest', 50, 60),
                    ('rest', 40, 50),
                    ('wait', 35, 40)]

        T, legs = pushed_up_rests_with_wait(**self.scenario_5)

        self.assertEqual(T, 35)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(leg, expected[i])

    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = pushed_up_rests_with_wait(**self.assertion_1)

if __name__ == '__main__':
    unittest.main()