from array import array
import pandas as pd

class TripInterval:

    def __init__(self, type, start, end):

        assert type in ['rest', 'duty', 'drive']

        self.type = type
        self.start = start
        self.end = end
        self.duration = end - start


def check_trip_sequence(seq):
    # TODO: return reason and index of failures
    duty_limit = 14
    drive_limit = 11
    rest_limit = 8

    duty_clock = 0
    drive_clock = 0

    for s, i in enumerate(seq):

        if s.type == 'drive':
            drive_clock += s.duration
            duty_clock += s.duration
            if drive_clock > drive_limit or duty_clock > duty_limit:
                return False

        if s.type == 'duty':
            duty_clock += s.duration
            if duty_clock > duty_limit:
                return False

        if s.type == 'rest':

            if s.duration == rest_limit:
                duty_clock = 0
                drive_clock = 0
            else:
                return False

    return True


class TimeWindow:

    def __init__(self, e, l):
        
        assert e <= l

        self.e = e
        self.l = l
        self.delta = l - e


class TripStats:

    DRIVE = 11
    DUTY = 14
    REST = 10

    def __init__(self, time_windows, travel_times):

        assert len(travel_times) == len(time_windows) - 1

        self.WINDOWS = time_windows
        self.TRAVEL_TIMES = travel_times

        self.N_STOPS = len(time_windows)


        self.nRests_between = array('h', (int(),)*(self.N_STOPS -1))  # number of rests between consecutive stops
        self.nRests = array('h', (int(),)*self.N_STOPS)               # number of rests at each stop

        self.remDrive_a = array('f', (float(),)*self.N_STOPS)
        self.remDrive_d = array('f', (float(),)*self.N_STOPS)
        self.remDuty_a = array('f', (float(),)*self.N_STOPS)
        self.remDuty_d = array('f', (float(),)*self.N_STOPS)

        self.t_a = array('f', (float(),)*self.N_STOPS)
        self.t_d = array('f', (float(),)*self.N_STOPS)

        self.t_a_shadow = array('f', (float(),)*self.N_STOPS)
        self.t_d_shadow = array('f', (float(),)*self.N_STOPS)

        self.slack_a = array('f', (float(),)*self.N_STOPS)
        self.slack_d = array('f', (float(),)*self.N_STOPS)

        self.wait = array('f', (float(),)*self.N_STOPS)
        self.tBest = array('f', (float(),)*self.N_STOPS)

        self.rest_push_end = list()

        self.t_d[-1] = self.WINDOWS[-1].l
        self.slack_d[-1] = self.WINDOWS[-1].delta
        self.remDrive_d[-1] = self.DRIVE
        self.remDuty_d[-1] = self.DUTY
        self.t_a[-1] = self.WINDOWS[-1].l

    def _report(self):

        df = pd.DataFrame([self.t_a,
                           self.slack_a,
                           self.remDrive_a,
                           self.remDuty_a,
                           self.tBest,
                           self.t_d,
                           self.slack_d,
                           self.remDrive_d,
                           self.remDuty_d,
                           self.wait,
                           self.nRests]).T
        df.columns = ['t_a','slack_a','remDrive_a','remDuty_a','tBest','t_d','slack_d','remDrive_d','remDuty_d','wait','nRests']
        df.sort_index(ascending=False, inplace=True)
        return df

    def print_report(self):

        rpt = self._report()
        with pd.option_context('display.max_rows', rpt.shape[0], 'display.max_columns', rpt.shape[1]):
            print(rpt)