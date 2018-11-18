from array import array
import math
from utils import TimeWindow
from copy import copy


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

        self.rest_push_end = int()

        self.t_d[-1] = self.WINDOWS[-1].l
        self.slack_d[-1] = self.WINDOWS[-1].delta
        self.remDrive_d[-1] = self.DRIVE
        self.remDuty_d[-1] = self.DUTY





# DRIVE = 11
# DUTY = 14
# REST = 10
#
WINDOWS = (TimeWindow(10,15), TimeWindow(3,18), TimeWindow(10,18), TimeWindow(15,35), TimeWindow(40,45), TimeWindow(75, 100), TimeWindow(75,100))
travel_times = (6,2,4,10,10,15)

TS = TripStats(WINDOWS, travel_times)

#
# nRests_between = [0]*len(travel_times)
# nRests = [0]*(len(travel_times) + 1)
# remDrive_a = [None]*(len(travel_times) + 1)
# remDrive_d = [None]*(len(travel_times) + 1)
# remDuty_a = [None]*(len(travel_times) + 1)
# remDuty_d = [None]*(len(travel_times) + 1)
# t_a = [None]*(len(travel_times) + 1)
# t_d = [None]*(len(travel_times) + 1)
# slack_a = [None]*(len(travel_times) + 1)
# slack_d = [None]*(len(travel_times) + 1)
# wait = [0]*(len(travel_times) + 1)
# tBest = [None]*(len(travel_times) + 1)
#
# # declare "shadow" variables
# t_a_shadow = [None]*(len(travel_times) + 1)
# t_d_shadow = [None]*(len(travel_times) + 1)
#
# rest_push_end = int()
#
# # initialize
# t_d[-1] = WINDOWS[-1].l
# slack_d[-1] = WINDOWS[-1].delta
# remDrive_d[-1] = 11
# remDuty_d[-1] = 14

def print_report(i):

    global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest


    arrive_message = '''
    At location {}: \n \t Arrival: t: {}, slack: {}, remDrive: {}, remDuty: {} \n \t Depart: tBest: {}, t: {}, slack: {}, remDrive: {}, remDuty: {}, wait: {}
    '''.format(i, t_a[i], slack_a[i], remDrive_a[i], remDuty_a[i], tBest[i], t_d[i], slack_d[i], remDrive_d[i], remDuty_d[i], wait[i])

    print(arrive_message)
    print('------')


def compute_arrival_time(ts, i):

    assert 0 <= i < ts.N_STOPS
    print(i)

    if ts.TRAVEL_TIMES[i] <= ts.remDrive_d[i + 1]:

        ts.t_a[i] = ts.t_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.remDrive_a[i] = ts.remDrive_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.remDuty_a[i] = ts.remDuty_a[i + 1] - ts.TRAVEL_TIMES[i]
        ts.slack_a[i] = ts.slack_d[i + 1]

    else:

        ts.nRests_between[i] = 1 + math.floor((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) / ts.DRIVE)
        ts.t_a[i] = ts.t_d[i + 1] - (ts.TRAVEL_TIMES[i] + ts.nRests_between[i] * ts.REST)
        ts.slack_a[i] = ts.slack_d[i + 1] + (ts.remDuty_d[i + 1] - ts.remDrive_d[i + 1]) + (ts.nRests_between[i] - 1) * (ts.DUTY - ts.DRIVE)
        ts.remDuty_a[i] = ts.DUTY - ((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) % ts.DRIVE)
        ts.remDrive_a[i] = ts.DRIVE - ((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) % ts.DRIVE)

    return ts



def backwards_search(ts, k, j, debug=False):

    for i in reversed(range(j, k+1)):

        #### Phase I: compute arrival time ####
        ts = compute_arrival_time(ts, i)

        #### Phase II: analyze arrival time ####

        # dispatch window violation
        if ts.t_a[i] < ts.WINDOWS[i].e:

            # Branch A
            return False, i, ts

        else:

            if ts.WINDOWS[i].e <= ts.t_a[i] <= ts.WINDOWS[i].l:

                # Branch B

                ts.slack_d[i] = min(ts.slack_a[i], ts.t_a[i] - ts.WINDOWS[i].e)
                ts.t_d[i] = copy(ts.t_a[i])
                ts.remDrive_d[i] = ts.remDrive_a[i]
                ts.remDuty_d[i] = ts.remDuty_a[i]


                if debug:
                    print("Branch: B")
                    print_report(i)


            else:

                ts.tBest[i] = ts.t_a[i] - ts.slack_a[i] - ts.remDuty_a[i]

                if ts.tBest[i] > ts.WINDOWS[i].l:

                    ts.nRests[i] = math.ceil((ts.tBest[i] - ts.WINDOWS[i].l)/(ts.DRIVE + ts.DUTY))
                    ts.wait[i] = max(ts.t_a[i] - ts.WINDOWS[i].l - ts.nRests[i]*ts.REST, 0)

                    if ts.tBest[i] - (ts.nRests[i]*ts.REST + (ts.nRests[i] - 1)*ts.DUTY) < ts.WINDOWS[i].l:

                        if ts.t_a[i] - ts.REST < ts.WINDOWS[i].l:

                            # time window violation
                            if ts.t_a[i] - ts.REST < ts.WINDOWS[i].l:
                                return False, i, ts

                            else:

                                ts.t_d[i] = ts.t_a[i] - ts.REST
                                ts.slack_d[i] = min(ts.t_d[i] - ts.WINDOWS[i].l, (ts.tBest[i] - (ts.nRests[i] * ts.REST + (ts.nRests[i] - 1) * ts.DUTY)))
                                ts.remDuty_d[i] = ts.DUTY
                                ts.remDrive_d[i] = ts.DRIVE
                                # adjust previous
                                ts.t_d_shadow[i + 1] = ts.t_d[i+1] - ts.slack_a[i]
                                ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                        else:

                            ts.t_d[i] = ts.WINDOWS[i].l
                            ts.slack_d[i] = min(ts.t_d[i] - ts.WINDOWS[i].l, (ts.tBest[i] - (ts.nRests[i]*ts.REST + (ts.nRests[i] - 1)*ts.DUTY)))
                            ts.remDuty_d[i] = ts.DUTY
                            ts.remDrive_d[i] = ts.DRIVE
                            # adjust previous
                            ts.t_d_shadow[i+1] = ts.t_d[i+1] - ts.slack_a[i]
                            ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                    else:
                        # adjust previous departure time
                        ts.t_d_shadow[i+1] = ts.t_d[i+1] - ts.slack_a[i]
                        ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                        ts.t_d[i] = ts.WINDOWS[i].l
                        ts.remDuty_d[i] = ts.DUTY - ((ts.tBest[i] - (ts.nRests[i]*ts.REST + (ts.nRests[i] - 1)*ts.DUTY)) - ts.WINDOWS[i].l)
                        ts.remDrive_d[i] = min(ts.remDuty_d[i], ts.DRIVE)
                        ts.slack_d[i] = 0

                else:

                    ts.wait[i] = ts.t_a[i] - ts.WINDOWS[i].l

                    # TODO: worked, check algo
                    if ts.wait[i] > ts.slack_a[i]:

                        # Branch C

                        # adjust previous departure time
                        ts.t_d_shadow[i+1] = ts.t_d[i+1] - ts.slack_a[i]
                        ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                        ts.slack_d[i] = 0
                        ts.remDuty_d[i] = ts.remDuty_a[i] - (ts.wait[i] - ts.slack_a[i])#- wait[i] - slack_a[i]
                        ts.remDrive_d[i] = min(ts.remDrive_a[i], ts.remDuty_d[i])
                        ts.t_d[i] = ts.WINDOWS[i].l


                        if debug:
                            print("Branch: C")
                            print_report(i)

                    else:
                        ts.slack_d[i] = min(ts.slack_a[i] - ts.wait[i], ts.WINDOWS[i].delta)

                        # adjust previous departure time
                        ts.t_d_shadow[i+1] = ts.t_d[i+1] - ts.slack_a[i]
                        ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]


                        ts.remDuty_d[i] = ts.remDuty_a[i]
                        ts.remDrive_d[i] = ts.remDrive_a[i]
                        ts.t_d[i] = ts.WINDOWS[i].l

                        if debug:
                            print("Branch: D")
                            print_report(i)
    return True, i, ts




def compute_nrests_between(ts, j, i):

    #global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest

    assert j < i

    nrests_ijs = 0
    nrests_ijb = 0

    # count all rests at stops j through i
    for k in range(j, i+1):
        nrests_ijs += ts.nRests[k]

    # count all rests between stops j and i
    # nRests_between[k] = rests taken between k and k+1
    for k in range(j, i):
        nrests_ijb += ts.nRests_between[k]

    return nrests_ijs + nrests_ijb, nrests_ijs, nrests_ijb


# def make_cache(i):
#     cache = dict()
#     cache['t_d'] = copy(t_d[i])
#     cache['wait'] = copy(wait[i])
#     cache['remDrive_d'] = copy(remDrive_d[i])
#     cache['remDuty_d'] = copy(remDuty_d[i])
#     cache['slack_d'] = copy(slack_d[i])
#     return cache
#
# def restore_cache(i, cache):
#     t_d[i] = cache['t_d']
#     wait[i] = cache['wait']
#     remDrive_d[i] = cache['remDrive_d']
#     remDuty_d[i] = cache['remDuty_d']
#     slack_d[i] = cache['slack_d']

def push_up_nearest_rest(ts, i, j):

    #global nRests, nRests_between

    assert j > i

    p = ts.nRests[i:(j+1)].index(1)
    q = ts.nRests_between[i:(j+1)].index(1)

    if p <= q:
        ts.nRests[i + p] = 0
    else:
        ts.nRests_between[i + q] = 0

    return ts







def restore(ts, i, debug=False):

    #global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest, rest_push_end

    #N = 6 # for testing only
    for j in range(i+1, ts.N_STOPS):

        nRests_ij, _ , _  = compute_nrests_between(ts, i, j)
        #print("Rests between {} and {}: {}, waits at {}: {}".format(i,j, nRests_ij, j, wait[j]))

        if ts.wait[j] > 0 and nRests_ij > 0:
            #print_report(j)
            ts.nRests[j] += 1

            ts = push_up_nearest_rest(ts, i, j)
            ts.rest_push_end = j

            #print("Rest push end: {}".format(rest_push_end))

            if ts.t_a[j] - ts.nRests[j]*ts.REST >= ts.WINDOWS[j].e:

                if ts.t_a[j] - (ts.nRests[j]*ts.REST) <= ts.WINDOWS[j].l:

                    # Branch B

                    ts.t_d[j] = ts.t_a[j] - ts.nRests[j]*ts.REST
                    ts.remDuty_d[j] = ts.DUTY
                    ts.remDrive_d[j] = ts.DRIVE
                    ts.wait[j] = 0
                    ts.slack_d[j] = min(ts.t_d[j] - ts.WINDOWS[j].e, ts.slack_a[j] + ts.remDuty_a[j] + (ts.nRests[j] - 1)*ts.REST)

                    if debug:
                        pass
                        #print("In Branch B at location {}".format(j))
                        #print_report(j)
                else:

                    # Branch A

                    ts.t_d[j] = ts.WINDOWS[j].l
                    ts.remDuty_d[j] = ts.DUTY
                    ts.remDrive_d[j] = ts.DRIVE
                    ts.wait[j] = ts.t_a[j] - ts.nRests[j]*ts.REST - ts.WINDOWS[j].l
                    ts.slack_d[j] = min(ts.WINDOWS[j].delta, ts.slack_a[j] + ts.remDuty_a[j] + (ts.nRests[j] -1)*ts.REST - (ts.t_a[j] - ts.nRests[j]*ts.REST - ts.WINDOWS[j].l))

                    if debug:
                        #print("In Branch A at location {}".format(j))
                        print_report(j)

            #print("In backwards search from {} to {}".format(j-1, i))
            status, placeholder_i, ts = backwards_search(ts, j-1, i, debug=False)
            #print("=========================")

            if ts.t_a[placeholder_i] >= ts.WINDOWS[placeholder_i].e: # before was i
                print("Done!!")
                return True, ts

            else:
                ts.nRests[j] -= 1

        else:
            continue

    return False, ts



def smart_trip(ts):

    j = ts.N_STOPS - 2
    print(j)
    while j > 0:
        status, i, ts = backwards_search(ts, j, 0)
        print(i)
        if status:
            return True, ts
        else:
            restore_status, ts = restore(ts, i)
            #print("restore called at {}".format(i))
        if restore_status:
            j = i - 1
        else:
            return False, ts

    return True, ts


#t = smart_trip()
# print(t)
#results = backwards_search(5,0, debug = False)
#status = restore(0, debug = False)
#print(rest_push_end)
#print(nRests_between)

# TODO: combine shadow with actual

# for i in range(rest_push_end + 1, 5):
#
#     if t_a_shadow[i] and t_d_shadow[i+1]:
#         t_a[i] = t_a_shadow[i]
#         t_d[i+1] = t_d_shadow[i+1]


# construct path
# using nRests, t_d, t_a


def construct_trip(ts):

    legs = list()

    for i in range(ts.rest_push_end + 1, ts.N_STOPS - 2):

        if ts.t_a_shadow[i] and ts.t_d_shadow[i+1]:
            ts.t_a[i] = ts.t_a_shadow[i]
            ts.t_d[i+1] = ts.t_d_shadow[i+1]


    T = ts.t_d[-1]

    for i in reversed(range(ts.N_STOPS-1)):

        if ts.nRests_between[i] > 0:
            legs.append(('drive', T - ts.remDrive_d[i + 1], T))

            T -= ts.remDrive_d[i+1]
            for rests in range(ts.nRests_between[i]):
                legs.append(('rest', T - 10, T))
                T -= 10
                print(T)
                legs.append(('drive', T - min(11, T - ts.t_a[i]), T))
                T -= min(T, T - ts.t_a[i])

        else:
            legs.append(('drive', ts.t_a[i], T))
            T -= T - ts.t_a[i]

        if ts.nRests[i] > 0:
            legs.append(('rest', T - 10*ts.nRests[i], T))
            T -= 10*ts.nRests[i]
        if ts.t_d[i] < T:
            legs.append(('wait', T - (ts.t_a[i] - ts.t_d[i]), T))
            T -= ts.t_a[i] - ts.t_d[i]

    return legs


WINDOWS = (TimeWindow(10,15), TimeWindow(3,18), TimeWindow(10,18), TimeWindow(15,35), TimeWindow(40,45), TimeWindow(75, 100), TimeWindow(75,100))
travel_times = (6,2,4,10,10,15)

TS = TripStats(WINDOWS, travel_times)


#_, ts = smart_trip(TS)
#temp = smart_trip(TS)
temp = backwards_search(TS, 5, 0)
temp = restore(temp[2], 0)
temp = construct_trip(temp[1])
print(temp)