import sys
import unittest
sys.path.append('..')
from utils import construct_trip, drive, wait_no_rest, rest_no_wait, pushed_up_rests_with_wait, rests_with_waits

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

        # Not enough rests given.
        cls.drive_senario_3b_input = {
            'T': 40,
            'legs': [],
            'nRests_between': 1,
            't_a': 5,
            'remDrive_d': 1
        }


    def test_senario_1a(self):

        output = [('drive', 15, 20)]

        T, legs = drive(T=self.drive_senario_1a_input['T'],
                        legs=self.drive_senario_1a_input['legs'],
                        nRests_between=self.drive_senario_1a_input['nRests_between'],
                        t_a=self.drive_senario_1a_input['t_a'],
                        remDrive_d=self.drive_senario_1a_input['remDrive_d'])


        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], output[i])

    def test_senario_1b(self):

        output = [('drive', 15, 20)]

        T, legs = drive(T=self.drive_senario_1b_input['T'],
                        legs=self.drive_senario_1b_input['legs'],
                        nRests_between=self.drive_senario_1b_input['nRests_between'],
                        t_a=self.drive_senario_1b_input['t_a'],
                        remDrive_d=self.drive_senario_1b_input['remDrive_d'])


        self.assertEqual(len(legs), 1)
        self.assertEqual(T, 15)

        for i, leg in enumerate(legs):
            with self.subTest(i=i):
                self.assertEqual(legs[i], output[i])

    def test_senario_2a(self):

        output = [('drive', 15, 20),
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
                self.assertEqual(legs[i], output[i])

    def test_senario_2b(self):

        output = [('drive', 35, 40),
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
                self.assertEqual(legs[i], output[i])

    def test_senario_2c(self):

        output = [('rest', 50, 60),
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
                self.assertEqual(legs[i], output[i])

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

# TODO: wait_no_rest
# TODO: rest_no_waits
# TODO: pushed_up_rests_with_wait
# TODO: rests_with_waits


if __name__ == '__main__':
    unittest.main()