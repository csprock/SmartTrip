import math
from copy import copy
from utils import DispatchWindowViolation

import logging

LOGGER = logging.getLogger(__name__)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(funcName)s] - %(message)")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)


def compute_arrival_time(ts, i):
    '''
    Phase I of Algorithm 2. Computes the arrival time at next destination,
    the remaining duty and drive time upon arrival, and the remaining slack.

    :param ts: TripStats object
    :param i: index of current location
    :return: modified TripStats object
    '''

    assert 0 <= i < ts.N_STOPS

    if ts.TRAVEL_TIMES[i] <= ts.remDrive_d[i + 1]:
        ts.t_a[i] = ts.t_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.remDrive_a[i] = ts.remDrive_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.remDuty_a[i] = ts.remDuty_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.slack_a[i] = ts.slack_d[i + 1]

    else:
        ts.nRests_between[i] = 1 + math.floor((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) / ts.DRIVE)
        ts.t_a[i] = ts.t_d[i + 1] - (ts.TRAVEL_TIMES[i] + ts.nRests_between[i] * ts.REST)
        ts.slack_a[i] = ts.slack_d[i + 1] + (ts.remDuty_d[i + 1] - ts.remDrive_d[i + 1]) + (ts.nRests_between[i] - 1) * (ts.DUTY - ts.DRIVE)
        ts.remDuty_a[i] = ts.DUTY - ((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) % ts.DRIVE)
        ts.remDrive_a[i] = ts.DRIVE - ((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) % ts.DRIVE)

    return ts


# TODO: set shadow variables to normal ones for non-slack branches
# TODO identify where slack is being updating in the pass-thru scenario
def analyze_arrival_info(ts, i):
    '''
    Phase II of Algorithm 2, analyzing the arrival time and computing the
    number of required rests ands waits

    :param ts: TripStats object
    :param i: index of current stop
    :return: modified TripStats object

    :raises: DispatchWindowViolation
    '''

    #### Phase II: analyze arrival time ####

    # dispatch window violation
    if ts.t_a[i] < ts.WINDOWS[i].e:

        # Branch A
        LOGGER.debug("Location: {}, Branch: {}".format(i, "A"))
        raise DispatchWindowViolation
        #return False, i, ts

    else:

        if ts.WINDOWS[i].e <= ts.t_a[i] <= ts.WINDOWS[i].l:

            # Branch B
            LOGGER.debug("Location: {}, Branch: {}".format(i, "B"))

            ts.slack_d[i] = min(ts.slack_a[i], ts.t_a[i] - ts.WINDOWS[i].e)
            ts.t_d[i] = copy(ts.t_a[i])
            ts.remDrive_d[i] = ts.remDrive_a[i]
            ts.remDuty_d[i] = ts.remDuty_a[i]

        else:

            ts.tBest[i] = ts.t_a[i] - ts.slack_a[i] - ts.remDuty_a[i]

            if ts.tBest[i] > ts.WINDOWS[i].l:

                ts.nRests[i] = math.ceil((ts.tBest[i] - ts.WINDOWS[i].l) / (ts.DRIVE + ts.DUTY))
                ts.wait[i] = max(ts.t_a[i] - ts.WINDOWS[i].l - ts.nRests[i] * ts.REST, 0)

                if ts.tBest[i] - (ts.nRests[i] * ts.REST + (ts.nRests[i] - 1) * ts.DUTY) < ts.WINDOWS[i].l:

                    if ts.t_a[i] - ts.REST < ts.WINDOWS[i].l:

                        # time window violation
                        if ts.t_a[i] - ts.REST < ts.WINDOWS[i].e:
                            LOGGER.debug("Location: {}, Branch: {}".format(i, "G"))
                            raise DispatchWindowViolation

                        else:

                            LOGGER.debug("Location: {}, Branch: {}".format(i, "H"))

                            ts.t_d[i] = ts.t_a[i] - ts.REST
                            ts.slack_d[i] = min(ts.t_d[i] - ts.WINDOWS[i].e, (ts.t_d[i] - (
                                        ts.tBest[i] - (ts.nRests[i] * ts.REST + (ts.nRests[i] - 1) * ts.DUTY))))
                            ts.remDuty_d[i] = ts.DUTY
                            ts.remDrive_d[i] = ts.DRIVE
                            # adjust previous departure time
                            ts.t_d_shadow[i + 1] = ts.t_d[i + 1] - ts.slack_a[i]
                            ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                    else:

                        LOGGER.debug("Location: {}, Branch: {}".format(i, "F"))

                        ts.t_d[i] = ts.WINDOWS[i].l
                        ts.slack_d[i] = min(ts.t_d[i] - ts.WINDOWS[i].e, (ts.t_d[i] - (
                                    ts.tBest[i] - (ts.nRests[i] * ts.REST + (ts.nRests[i] - 1) * ts.DUTY))))
                        ts.remDuty_d[i] = ts.DUTY
                        ts.remDrive_d[i] = ts.DRIVE
                        # adjust previous departure_time
                        ts.t_d_shadow[i + 1] = ts.t_d[i + 1] - ts.slack_a[i]
                        ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                else:

                    LOGGER.debug("Location: {}, Branch: {}".format(i, "E"))

                    # adjust previous departure time
                    ts.t_d_shadow[i + 1] = ts.t_d[i + 1] - ts.slack_a[i]
                    ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                    ts.t_d[i] = ts.WINDOWS[i].l
                    ts.remDuty_d[i] = ts.DUTY - ((ts.tBest[i] - (ts.nRests[i] * ts.REST + (ts.nRests[i] - 1) * ts.DUTY)) - ts.WINDOWS[i].l)
                    ts.remDrive_d[i] = min(ts.remDuty_d[i], ts.DRIVE)
                    ts.slack_d[i] = 0

            else:

                ts.wait[i] = ts.t_a[i] - ts.WINDOWS[i].l

                if ts.wait[i] > ts.slack_a[i]:

                    # Branch C

                    LOGGER.debug("Location: {}, Branch: {}".format(i, "C"))

                    # adjust previous departure time
                    ts.t_d_shadow[i + 1] = ts.t_d[i + 1] - ts.slack_a[i]
                    ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                    ts.slack_d[i] = 0
                    ts.remDuty_d[i] = ts.remDuty_a[i] - (ts.wait[i] - ts.slack_a[i])  # - wait[i] - slack_a[i]
                    ts.remDrive_d[i] = min(ts.remDrive_a[i], ts.remDuty_d[i])
                    ts.t_d[i] = ts.WINDOWS[i].l


                else:

                    # Branch D
                    LOGGER.debug("Location: {}, Branch: {}".format(i, "D"))

                    ts.slack_d[i] = min(ts.slack_a[i] - ts.wait[i], ts.WINDOWS[i].delta)

                    # adjust previous departure time
                    ts.t_d_shadow[i + 1] = ts.t_d[i + 1] - ts.slack_a[i]
                    ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                    ts.remDuty_d[i] = ts.remDuty_a[i]
                    ts.remDrive_d[i] = ts.remDrive_a[i]
                    ts.t_d[i] = ts.WINDOWS[i].l

    ts.last_stop = i

    return ts


def backwards_search(ts, k, j):
    '''
    Algorithm 2 in Archetti and Savelsbergh (2014).

    :param ts: TripStats object
    :param k: location where to begin backwards search
    :param j: location where to terminate backwards search
    :return: status, last index, modified TripStats object
    '''

    for i in reversed(range(j, k+1)):

        #### Phase I: compute arrival time ####
        ts = compute_arrival_time(ts, i)

        #### Phase II: analyze arrival time ####
        try:
            ts = analyze_arrival_info(ts, i)
        except DispatchWindowViolation:
            return False, i, ts

    return True, i, ts


def compute_nrests_between(ts, j, i):
    '''
    Computes the number of rests between stops j and i (inclusive of stops
    at j and i).

    :param ts: TripStats object
    :param j: first stop
    :param i: next stop
    :return:
        - total stops
        - number of rests at stops between j and i (inclusive),
        - number of rests between stops between j and i (inclusive)
    '''

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


def smallest_nonzero(arr):

    for k, v in enumerate(arr):
        if v > 0:
            return k


def push_up_nearest_rest(ts, i, j):
    '''
    Finds the closest rest between i and j and
    sets it to zero (restore() sets moves location
    of this rest further up)

    :param ts: TripStats
    :param i: first stop
    :param j: next stop
    :return: modified TripStats object
    '''

    assert j > i

    #p = ts.nRests[i:(j+1)].index(1)
    #q = ts.nRests_between[i:(j+1)].index(1)

    p = smallest_nonzero(ts.nRests[i:(j + 1)])
    q = smallest_nonzero(ts.nRests_between[i:(j + 1)])

    if p <= q:
        ts.nRests[i + p] = 0
    else:
        ts.nRests_between[i + q] = 0

    return ts #TODO: return min(p, q)


def analyze_rest(ts, j):

    if ts.t_a[j] - (ts.nRests[j] * ts.REST) <= ts.WINDOWS[j].l:

        # Branch B
        LOGGER.debug("In Branch B at location {}".format(j))

        ts.t_d[j] = ts.t_a[j] - ts.nRests[j] * ts.REST
        ts.remDuty_d[j] = ts.DUTY
        ts.remDrive_d[j] = ts.DRIVE
        ts.wait[j] = 0
        ts.slack_d[j] = min(ts.t_d[j] - ts.WINDOWS[j].e, ts.slack_a[j] + ts.remDuty_a[j] + (ts.nRests[j] - 1) * ts.REST)


    else:

        LOGGER.debug("In Branch A at location {}".format(j))

        ts.t_d[j] = ts.WINDOWS[j].l
        ts.remDuty_d[j] = ts.DUTY
        ts.remDrive_d[j] = ts.DRIVE
        ts.wait[j] = ts.t_a[j] - ts.nRests[j] * ts.REST - ts.WINDOWS[j].l
        ts.slack_d[j] = min(ts.WINDOWS[j].delta, ts.slack_a[j] + ts.remDuty_a[j] + (ts.nRests[j] - 1) * ts.REST - (
                    ts.t_a[j] - ts.nRests[j] * ts.REST - ts.WINDOWS[j].l))

    return ts


# TODO: refactor logic in main look into separate function
def restore(ts, i):
    '''
    Executes Algorithm 3 in Archetti and Savelsbergh (2014).

    :param ts: TripStats object
    :param i: index of stop from where to begin restore()
    :return: stats, modified TripStats object
    '''

    for j in range(i+1, ts.N_STOPS):

        nRests_ij, _ , _  = compute_nrests_between(ts, i, j)
        #print("Rests between {} and {}: {}, waits at {}: {}".format(i,j, nRests_ij, j, wait[j]))

        if ts.wait[j] > 0 and nRests_ij > 0:

            ts.nRests[j] += 1

            ts = push_up_nearest_rest(ts, i, j)
            ts.rest_push_end.append(j)

            #LOGGER.debug("Rest push end: {}".format(ts.rest_push_end))

            if ts.t_a[j] - ts.nRests[j]*ts.REST >= ts.WINDOWS[j].e:

                ts = analyze_rest(ts, j)

            LOGGER.debug("In backwards search from {} to {}".format(j-1, i))

            status, placeholder_i, ts = backwards_search(ts, j-1, i)

            if ts.t_a[placeholder_i] >= ts.WINDOWS[placeholder_i].e: # before was i
                LOGGER.debug("Done!")
                return True, ts

            else:
                ts.nRests[j] -= 1
                ts.rest_push_end.pop(-1)

        else:
            continue

    return False, ts

def smart_trip(ts):
    '''
    Main execution loop for Algorithm 1 in Archetti & Savelsbergh (2014)

    :param ts: TripStats object
    :return: status, modified TripStats object
    '''

    j = ts.N_STOPS - 2
    while j > 0:
        status, i, ts = backwards_search(ts, j, 0)
        if status:
            return True, ts
        else:
            restore_status, ts = restore(ts, i)
        if restore_status:
            j = i - 1
        else:
            return False, ts

    return True, ts