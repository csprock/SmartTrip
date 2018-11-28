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
        cls.drive_senario_1a_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 0,
            't_a': 15,
            'remDrive_d': 6
        }

        # No rests between driving, remDrive_d == time remaining to destination
        cls.drive_senario_1b_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 0,
            't_a': 15,
            'remDrive_d': 5
        }

        #### Rests between driving ####
        # 1 rest between driving
        cls.drive_senario_2a_input = {
            'T': 20,
            'legs': [],
            'nRests_between': 1,
            't_a': 0,
            'remDrive_d': 5
        }

        # multiple rests between driving
        cls.drive_senario_2b_input = {
            'T': 40,
            'legs': [],
            'nRests_between': 2,
            't_a': 0,
            'remDrive_d': 5
        }

        # start driving without any remaining drive time
        cls.drive_senario_2c_input = {
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
        cls.drive_senario_3b_input = {
            'T': 40,
            'legs': [],
            'nRests_between': 1,
            't_a': 5,
            'remDrive_d': 1
        }


    def test_senario_1a(self):

        expected = [('drive', 15, 20)]

        T, legs = drive(T=self.drive_senario_1a_input['T'],
                        legs=self.drive_senario_1a_input['legs'],
                        nRests_between=self.drive_senario_1a_input['nRests_between'],
                        t_a=self.drive_senario_1a_input['t_a'],
                        remDrive_d=self.drive_senario_1a_input['remDrive_d'])


        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_senario_1b(self):

        expected = [('drive', 15, 20)]

        T, legs = drive(T=self.drive_senario_1b_input['T'],
                        legs=self.drive_senario_1b_input['legs'],
                        nRests_between=self.drive_senario_1b_input['nRests_between'],
                        t_a=self.drive_senario_1b_input['t_a'],
                        remDrive_d=self.drive_senario_1b_input['remDrive_d'])


        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_senario_2a(self):

        expected = [('drive', 15, 20),
                  ('rest', 5, 15),
                  ('drive', 0, 5)]

        T, legs = drive(T=self.drive_senario_2a_input['T'],
                        legs=self.drive_senario_2a_input['legs'],
                        nRests_between=self.drive_senario_2a_input['nRests_between'],
                        t_a=self.drive_senario_2a_input['t_a'],
                        remDrive_d=self.drive_senario_2a_input['remDrive_d'])

        self.assertEqual(len(legs), 3)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_senario_2b(self):

        expected = [('drive', 35, 40),
                  ('rest', 25, 35),
                  ('drive', 14, 25),
                  ('rest', 4, 14),
                  ('drive', 0, 4)]

        T, legs = drive(T=self.drive_senario_2b_input['T'],
                        legs=self.drive_senario_2b_input['legs'],
                        nRests_between=self.drive_senario_2b_input['nRests_between'],
                        t_a=self.drive_senario_2b_input['t_a'],
                        remDrive_d=self.drive_senario_2b_input['remDrive_d'])

        self.assertEqual(len(legs), 5)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_senario_2c(self):

        expected = [('rest', 50, 60),
                  ('drive', 39, 50),
                  ('rest', 29, 39),
                  ('drive', 18, 29),
                  ('rest', 8, 18),
                  ('drive', 0, 8)]

        T, legs = drive(T=self.drive_senario_2c_input['T'],
                        legs=self.drive_senario_2c_input['legs'],
                        nRests_between=self.drive_senario_2c_input['nRests_between'],
                        t_a=self.drive_senario_2c_input['t_a'],
                        remDrive_d=self.drive_senario_2c_input['remDrive_d'])

        self.assertEqual(len(legs), 6)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_senario_3a(self):

        # TODO: create regex match and use assertRaisesRegex
        with self.assertRaises(ValueError):

            _, _ = drive(T=self.drive_senario_3a_input['T'],
                         legs=self.drive_senario_3a_input['legs'],
                         nRests_between=self.drive_senario_3a_input['nRests_between'],
                         t_a=self.drive_senario_3a_input['t_a'],
                         remDrive_d=self.drive_senario_3a_input['remDrive_d'])

    def test_senario_3a(self):

        # TODO: create regex match and use assertRaisesRegex
        with self.assertRaises(ValueError):

            T, legs = drive(T=self.drive_senario_3b_input['T'],
                            legs=self.drive_senario_3b_input['legs'],
                            nRests_between=self.drive_senario_3b_input['nRests_between'],
                            t_a=self.drive_senario_3b_input['t_a'],
                            remDrive_d=self.drive_senario_3b_input['remDrive_d'])


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

        T, legs = wait_no_rest(T=self.scenario_1_input['T'],
                               legs=self.scenario_1_input['legs'],
                               t_d=self.scenario_1_input['t_d'],
                               t_a=self.scenario_1_input['t_a'])

        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 3)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = wait_no_rest(T=self.assertion_1_input['T'],
                         legs=self.assertion_1_input['legs'],
                         t_d=self.assertion_1_input['t_d'],
                         t_a=self.assertion_1_input['t_a'])

    def test_assertion_2(self):

        with self.assertRaises(AssertionError):

            _, _ = wait_no_rest(T=self.assertion_2_input['T'],
                         legs=self.assertion_2_input['legs'],
                         t_d=self.assertion_2_input['t_d'],
                         t_a=self.assertion_2_input['t_a'])

    def test_assertion_3(self):

        with self.assertRaises(AssertionError):

            _, _ = wait_no_rest(T=self.assertion_3_input['T'],
                         legs=self.assertion_3_input['legs'],
                         t_d=self.assertion_3_input['t_d'],
                         t_a=self.assertion_3_input['t_a'])


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

        T, legs = rest_no_wait(T=self.scenario_1['T'],
                               legs=self.scenario_1['legs'],
                               nRests=self.scenario_1['nRests'])

        self.assertEqual(len(legs), 2)
        self.assertEqual(T, 0)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])


    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = rest_no_wait(T=self.assertion_1['T'],
                                legs=self.assertion_1['legs'],
                                nRests=self.assertion_1['nRests'])

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

        # multiple rests, no remDuty
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

        T, legs = rests_with_waits(T=self.scenario_1_input['T'],
                                   legs=self.scenario_1_input['legs'],
                                   nRests=self.scenario_1_input['nRests'],
                                   t_d=self.scenario_1_input['t_d'],
                                   remDuty_a=self.scenario_1_input['remDuty_a'],
                                   wait=self.scenario_1_input['wait'])

        self.assertEqual(len(legs), 3)
        self.assertEqual(T, 10)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_scenario_2(self):

        expected = [('wait', 26, 29),
                    ('rest', 16, 26)]

        T, legs = rests_with_waits(T=self.scenario_2_input['T'],
                                   legs=self.scenario_2_input['legs'],
                                   nRests=self.scenario_2_input['nRests'],
                                   t_d=self.scenario_2_input['t_d'],
                                   remDuty_a=self.scenario_2_input['remDuty_a'],
                                   wait=self.scenario_2_input['wait'])

        self.assertEqual(len(legs), 2)
        self.assertEqual(T, 16)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_scenario_3(self):

        expected = [('rest', 19, 29),
                    ('wait', 15, 19)]

        T, legs = rests_with_waits(T=self.scenario_3_input['T'],
                                   legs=self.scenario_3_input['legs'],
                                   nRests=self.scenario_3_input['nRests'],
                                   t_d=self.scenario_3_input['t_d'],
                                   remDuty_a=self.scenario_3_input['remDuty_a'],
                                   wait=self.scenario_3_input['wait'])

        self.assertEqual(len(legs), 2)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_scenario_4(self):

        expected = [('wait', 86, 90),
                    ('rest', 76, 86),
                    ('wait', 62, 76),
                    ('rest', 52, 62),
                    ('wait', 44, 52)]

        T, legs = rests_with_waits(T=self.scenario_4_input['T'],
                                   legs=self.scenario_4_input['legs'],
                                   nRests=self.scenario_4_input['nRests'],
                                   t_d=self.scenario_4_input['t_d'],
                                   remDuty_a=self.scenario_4_input['remDuty_a'],
                                   wait=self.scenario_4_input['wait'])

        self.assertEqual(len(legs), 5)
        self.assertEqual(T, 44)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_scenario_5(self):

        expected = [('rest', 80, 90),
                    ('wait', 66, 80),
                    ('rest', 56, 66),
                    ('wait', 54, 56)]

        T, legs = rests_with_waits(T=self.scenario_5_input['T'],
                                   legs=self.scenario_5_input['legs'],
                                   nRests=self.scenario_5_input['nRests'],
                                   t_d=self.scenario_5_input['t_d'],
                                   remDuty_a=self.scenario_5_input['remDuty_a'],
                                   wait=self.scenario_5_input['wait'])

        self.assertEqual(len(legs), 4)
        self.assertEqual(T, 54)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])

    def test_scenario_6(self):

        expected = [('rest', 80, 90),
                    ('wait', 66, 80),
                    ('rest', 56, 66)]

        T, legs = rests_with_waits(T=self.scenario_6_input['T'],
                                   legs=self.scenario_6_input['legs'],
                                   nRests=self.scenario_6_input['nRests'],
                                   t_d=self.scenario_6_input['t_d'],
                                   remDuty_a=self.scenario_6_input['remDuty_a'],
                                   wait=self.scenario_6_input['wait'])

        self.assertEqual(len(legs), 3)
        self.assertEqual(T, 56)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], expected[i])


    def test_assertion_1(self):

        with self.assertRaises(AssertionError):

            _, _ = rests_with_waits(T=self.assertion_1['T'],
                                legs=self.assertion_1['legs'],
                                nRests=self.assertion_1['nRests'],
                                t_d=self.assertion_1['t_d'],
                                remDuty_a=self.assertion_1['remDuty_a'],
                                wait=self.assertion_1['wait'])


# TODO: pushed_up_rests_with_wait

if __name__ == '__main__':
    unittest.main()