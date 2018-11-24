from utils import TimeWindow, TripInterval, TripStats
from tsp import backwards_search, restore, smart_trip, compute_arrival_time, compute_nrests_between, push_up_nearest_rest, smallest_nonzero

# def construct_trip(ts):
#
#     legs = list()
#
#     # for i in range(ts.N_STOPS):
#     #
#     #     if ts.t_a_shadow[i] > 0 and ts.t_d_shadow[i+1] > 0:
#     #         ts.t_a[i] = ts.t_a_shadow[i]
#     #         ts.t_d[i+1] = ts.t_d_shadow[i+1]
#
#
#     T = ts.t_d[-1]
#
#     for i in reversed(range(ts.N_STOPS-1)):
#
#         ## Execute rest/drive intervals during driving
#
#         if ts.nRests_between[i] > 0:
#             # execute remaining drive
#             legs.append(('drive', T - ts.remDrive_d[i + 1], T, i+1))
#             T -= ts.remDrive_d[i+1]
#
#             # execute drive-rest intervals
#             for rests in range(ts.nRests_between[i]):
#                 legs.append(('rest', T - 10, T, i+1))
#                 T -= 10
#                 legs.append(('drive', T - min(11, T - ts.t_a[i]), T, i+1))
#                 T -= min(11, T - ts.t_a[i])
#
#         else:
#             legs.append(('drive', ts.t_a[i], T, i+1))
#             T -= T - ts.t_a[i]
#
#         # Execute rest/wait intervals at destination
#
#         if i in ts.rest_push_end:
#             pushed_up_rest = True
#         else:
#             pushed_up_rest = False
#
#         if ts.nRests[i] > 0:
#
#             if ts.remDuty_a[i] > 0 and ts.wait[i] > 0:
#
#                 legs.append(('wait', T - min(ts.remDuty_a[i], ts.wait[i]), T, i+1))
#                 #print("First Rest", (T - min(ts.remDuty_a[i], ts.wait[i]), T))
#                 T -= min(ts.remDuty_a[i], ts.wait[i])
#
#             for r in range(ts.nRests[i]):
#                 legs.append(('rest', T - 10, T, -1))
#                 T -= 10
#
#                 # TODO: if pushed_up_rest is true, make last two rests consecutive
#                 if r == ts.nRests[i] - 2 and pushed_up_rest:
#                     legs.append(('rest', T - 10, T, -1))
#                     T -= 10
#
#                     if T > ts.t_d[i]:
#                         legs.append(('wait', T - min(14, T - ts.t_d[i]), T, i+1))
#
#                         #print("{} wait".format(r), (T - min(14, T - ts.t_d[i]), T))
#                         T -= min(14, T - ts.t_d[i])
#
#                     break
#
#
#                 else:
#                     if T > ts.t_d[i]:
#                         legs.append(('wait', T - min(14, T - ts.t_d[i]), T, i+1))
#
#                         #print((T - min(14, T - ts.t_d[i]), T))
#
#                         T -= min(14, T - ts.t_d[i])
#
#         elif ts.wait[i] > 0:
#             legs.append(('wait', T - ts.wait[i], T, i+1))
#             T -= ts.wait[i]
#
#     return legs

# def distribute_rests(legs, nRests, remDuty_a, wait, t_d, T, i, pushed_up_rest=False):
#     print(i)
#     #legs = list()
#     if remDuty_a > 0:
#         legs.append(('wait', T - min(remDuty_a, wait), T, i))
#         T -= min(remDuty_a, wait)
#
#     for r in range(nRests):
#         legs.append(('rest', T - 10, T, -1))
#         T -= 10
#
#         # TODO: if pushed_up_rest is true, make last two rests consecutive
#         if r == nRests - 2 and pushed_up_rest:
#             legs.append(('rest', T - 10, T, -1))
#             T -= 10
#
#             if T > t_d:
#                 legs.append(('wait', T - min(14, T - t_d), T, i))
#                 T -= min(14, T - t_d)
#
#             return legs, T
#         else:
#             if T > t_d:
#                 legs.append(('wait', T - min(14, T-t_d), T, i))
#                 T -= min(14, T-t_d)
#
#     return legs, T

def construct_trip(ts):

    legs = list()
    T = ts.t_a[-1]

    if ts.t_d[-1] < ts.t_a[-1]:
        legs.append(('wait', T - ts.t_d[-1], T))
        T -= ts.t_d[-1]

    for i in reversed(range(ts.N_STOPS - 1)):

        T, legs = drive(T, legs, ts.nRests_between[i], ts.t_a[i], ts.remDrive_d[i+1])

        if ts.wait[i] and ts.nRests[i]:
            if i in ts.rest_push_end:
                T, legs = pushed_up_rests_with_wait(T, legs, ts.nRests[i], ts.t_d[i], ts.remDuty_a[i])
            else:
                T, legs = rests_with_waits(T, legs, ts.nRests[i], ts.t_d[i], ts.remDuty_a[i])
        elif not ts.wait[i] and ts.nRests[i]:
            T, legs = rest_no_wait(T, legs, ts.nRests[i])
        elif ts.wait[i] and not ts.nRests[i]:
            T, legs = wait_no_rest(T, legs, ts.t_d[i], ts.t_a[i])
        else:
            pass

    return T, legs


def drive(T, legs, nRests_between, t_a, remDrive_d):

    if remDrive_d > 0:
        legs.append(('drive', T - min(11, remDrive_d, T - t_a), T))
        T -= min(11, remDrive_d, T - t_a)

    if nRests_between > 0:
        for r in range(nRests_between):
            legs.append(('rest', T - 10, T))
            T -= 10
            legs.append(('drive', T - min(11, T - t_a), T))
            T -= min(11, T - t_a)

    return T, legs

def wait_no_rest(T, legs, t_d, t_a):
    legs.append(('wait', T - (t_a - t_d), T))
    T -= t_a - t_d
    return T, legs

def rest_no_wait(T, legs, nRests):
    for r in range(nRests):
        legs.append(('rest', T - 10, T))
        T -= 10

    return T, legs

def pushed_up_rests_with_wait(T, legs, nRests, t_d, remDuty_d):

    if remDuty_d > 0:
        legs.append(('wait', T - remDuty_d, T))
        T -= remDuty_d

    for r in range(nRests):
        if r == nRests - 2:
            for j in range(2):
                legs.append(('rest', T - 10, T))
                T -= 10
            return T, legs
        else:
            legs.append(('rest', T - 10, T))
            T -= 10
            if T > t_d:
                legs.append(('rest', T - min(14, t_d), T))
                T -= min(14, t_d)

    return T, legs

def rests_with_waits(T, legs, nRests, t_d, remDuty_d):

    if remDuty_d > 0:
        legs.append(('wait', T - remDuty_d, T))
        T -= remDuty_d

    for r in range(nRests):
        legs.append(('rest', T - 10, T))
        T -= 10
        if T > t_d:
            legs.append(('wait', T - min(14, T - t_d), T))
            T -= min(14, T - t_d)

    return T, legs



# WINDOWS = (TimeWindow(10,15), TimeWindow(3,18), TimeWindow(10,18), TimeWindow(15,35), TimeWindow(40,45), TimeWindow(75, 100), TimeWindow(75,100))
# travel_times = (6,2,4,10,10,15)
# TS = TripStats(WINDOWS, travel_times)

# WINDOWS = (TimeWindow(2,25),
#            TimeWindow(10, 16),
#            TimeWindow(1, 24),
#            TimeWindow(33,33))
# travel_times = (4, 4, 5)
# #
# TS = TripStats(WINDOWS, travel_times)

#
# WINDOWS = (TimeWindow(2, 10),
#            TimeWindow(5, 10),
#            TimeWindow(40,40))
# travel_times = (5, 10)
#
# TS = TripStats(WINDOWS, travel_times)

# WINDOWS = (TimeWindow(1, 10),
#            TimeWindow(5, 10),
#            TimeWindow(40,40))
# travel_times = (9, 10)
#
# TS = TripStats(WINDOWS, travel_times)

# WINDOWS = (TimeWindow(0,10), TimeWindow(5,9), TimeWindow(40,40))
#
# travel_times = (9,10)
#
# TS = TripStats(WINDOWS, travel_times)

WINDOWS = tuple(reversed((TimeWindow(100,100),
           TimeWindow(70,70),
           TimeWindow(61,70),
           TimeWindow(50,53),
           TimeWindow(20,20),
           TimeWindow(11,20))))

travel_times = (9,10,1,9,10)

TS = TripStats(WINDOWS, travel_times)

print(TS.N_STOPS)
#_, ts = smart_trip(TS)
temp = smart_trip(TS)
construct_trip(temp[1])

#temp = backwards_search(TS, 1, 0)
#temp = restore(temp[2], 3)
# temp = backwards_search(temp[1], 2, 0)
# temp = restore(temp[2], 0)

# temp[1].print_report()
