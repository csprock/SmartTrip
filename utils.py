from array import array
import pandas as pd

class DispatchWindowViolation(Exception):
    pass

class TripInterval:

    def __init__(self, type, start, end):

        assert type in ['rest', 'duty', 'drive']

        self.type = type
        self.start = start
        self.end = end
        self.duration = end - start


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

        self.last_stop = len(time_windows) - 1

    def get_report(self):

        self.df = pd.DataFrame([self.t_a,
                           self.slack_a,
                           self.remDrive_a,
                           self.remDuty_a,
                           self.tBest,
                           self.t_d,
                           self.slack_d,
                           self.remDrive_d,
                           self.remDuty_d,
                           self.wait,
                           self.nRests,
                           self.t_a_shadow,
                           self.t_d_shadow]).T
        self.df.columns = ['t_a','slack_a','remDrive_a','remDuty_a','tBest','t_d','slack_d','remDrive_d','remDuty_d','wait','nRests', 't_a_shadow', 't_d_shadow']
        self.df.sort_index(ascending=False, inplace=True)
        return self.df

    def print_report(self):

        rpt = self.get_report()
        with pd.option_context('display.max_rows', rpt.shape[0], 'display.max_columns', rpt.shape[1]):
            print(rpt)


###########################################
##### Trip reconstruction functions #######
###########################################

# TODO move into TripStats class
def construct_trip(ts):

    legs = list()
    last_stop = ts.N_STOPS - 1

    T = ts.t_a[-1]

    if ts.t_d[-1] < ts.t_a[-1]:
        legs.append(('wait', T - ts.t_d[-1], T, -1))
        T -= ts.t_d[-1]

    for i in reversed(range(ts.N_STOPS - 1)):

        if i == ts.last_stop - 2:
            return T, legs

        T, legs = drive(T, legs, last_stop, ts.nRests_between[i], ts.t_a[i], ts.remDrive_d[i+1])
        last_stop -= 1

        if ts.wait[i] and ts.nRests[i]:
            if i in ts.rest_push_end:
                T, legs = pushed_up_rests_with_wait(T, legs, ts.nRests[i], ts.t_d[i], ts.remDuty_a[i], ts.wait[i])
            else:
                T, legs = rests_with_waits(T, legs, ts.nRests[i], ts.t_d[i], ts.remDuty_a[i], ts.wait[i])
        elif not ts.wait[i] and ts.nRests[i]:
            T, legs = rest_no_wait(T, legs, ts.nRests[i])
        elif ts.wait[i] and not ts.nRests[i]:
            T, legs = wait_no_rest(T, legs, ts.t_d[i], ts.t_a[i])
        else:
            pass

    return T, legs


def drive(T, legs, last_stop, nRests_between, t_a, remDrive_d):

    assert remDrive_d >= T - t_a or nRests_between > 0
    assert T - t_a <= remDrive_d + nRests_between*10 + max(0, (nRests_between - 1)*11) + 11

    if remDrive_d > 0:
        legs.append(('drive', T - min(11, remDrive_d, T - t_a), T, last_stop))
        T -= min(11, remDrive_d, T - t_a)

    if nRests_between > 0:
        for r in range(nRests_between):
            legs.append(('rest', T - 10, T, last_stop))
            T -= 10
            legs.append(('drive', T - min(11, T - t_a), T, last_stop))
            T -= min(11, T - t_a)

    return T, legs


def wait_no_rest(T, legs, t_d, t_a):

    assert t_d < t_a
    assert t_a - t_d <= 14
    assert T == t_a

    legs.append(('wait', T - (t_a - t_d), T, -1))
    T -= t_a - t_d

    return T, legs


def rest_no_wait(T, legs, nRests):

    assert nRests > 0

    for r in range(nRests):
        legs.append(('rest', T - 10, T, -1))
        T -= 10

    return T, legs


def pushed_up_rests_with_wait(T, legs, nRests, t_d, remDuty_d, wait):

    assert T - t_d == 10*nRests + wait

    if remDuty_d > 0:
        legs.append(('wait', T - min(remDuty_d, wait), T, -1))
        T -= min(remDuty_d, wait)

    for r in range(nRests):
        if r == nRests - 2:
            for j in range(2):
                legs.append(('rest', T - 10, T, -1))
                T -= 10

            if T > t_d:
                legs.append(('wait', T - (T - t_d), T, -1))
                T -= (T - t_d)

            return T, legs

        else:
            legs.append(('rest', T - 10, T, -1))
            T -= 10
            if T > t_d:
                legs.append(('wait', T - min(14, T - t_d), T, -1))
                T -= min(14, T - t_d)

    return T, legs


def rests_with_waits(T, legs, nRests, t_d, remDuty_a, wait):

    assert T - t_d == 10*nRests + wait

    if remDuty_a > 0:
        legs.append(('wait', T - min(remDuty_a, wait), T, -1))
        T -= min(remDuty_a, wait)

    for r in range(nRests):
        legs.append(('rest', T - 10, T, -1))
        T -= 10
        if T > t_d:
            legs.append(('wait', T - min(14, T - t_d), T, -1))
            T -= min(14, T - t_d)

    return T, legs


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
