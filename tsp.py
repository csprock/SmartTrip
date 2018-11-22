import math
from copy import copy



def print_report(ts, i):


    arrive_message = '''
    At location {}: \n \t Arrival: t: {}, slack: {}, remDrive: {}, remDuty: {} \n \t Depart: tBest: {}, t: {}, slack: {}, remDrive: {}, remDuty: {}, wait: {}
    '''.format(i, ts.t_a[i], ts.slack_a[i], ts.remDrive_a[i], ts.remDuty_a[i], ts.tBest[i], ts.t_d[i], ts.slack_d[i], ts.remDrive_d[i], ts.remDuty_d[i], ts.wait[i])
    print(arrive_message)
    print('------')


def compute_arrival_time(ts, i):

    assert 0 <= i < ts.N_STOPS

    if ts.TRAVEL_TIMES[i] <= ts.remDrive_d[i + 1]:

        ts.t_a[i] = ts.t_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.remDrive_a[i] = ts.remDrive_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.remDuty_a[i] = ts.remDuty_d[i + 1] - ts.TRAVEL_TIMES[i]
        ts.slack_a[i] = ts.slack_d[i + 1]

        #print(" travel time <= remDrive")
        #print_report(ts, i)

    else:

        ts.nRests_between[i] = 1 + math.floor((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) / ts.DRIVE)
        ts.t_a[i] = ts.t_d[i + 1] - (ts.TRAVEL_TIMES[i] + ts.nRests_between[i] * ts.REST)
        ts.slack_a[i] = ts.slack_d[i + 1] + (ts.remDuty_d[i + 1] - ts.remDrive_d[i + 1]) + (ts.nRests_between[i] - 1) * (ts.DUTY - ts.DRIVE)
        ts.remDuty_a[i] = ts.DUTY - ((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) % ts.DRIVE)
        ts.remDrive_a[i] = ts.DRIVE - ((ts.TRAVEL_TIMES[i] - ts.remDrive_d[i + 1]) % ts.DRIVE)

        #print(" travel time > remDrive")
        #print_report(ts, i)

    return ts



def backwards_search(ts, k, j, debug=False):

    for i in reversed(range(j, k+1)):

        #### Phase I: compute arrival time ####
        ts = compute_arrival_time(ts, i)

        #### Phase II: analyze arrival time ####

        # dispatch window violation
        if ts.t_a[i] < ts.WINDOWS[i].e:

            # Branch A
            print("Location: {}, Branch: {}".format(i, "A"))

            return False, i, ts

        else:

            if ts.WINDOWS[i].e <= ts.t_a[i] <= ts.WINDOWS[i].l:

                # Branch B
                print("Location: {}, Branch: {}".format(i, "B"))

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
                            if ts.t_a[i] - ts.REST < ts.WINDOWS[i].e:
                                print("Location: {}, Branch: {}".format(i, "G"))
                                return False, i, ts

                            else:

                                print("Location: {}, Branch: {}".format(i, "H"))

                                ts.t_d[i] = ts.t_a[i] - ts.REST
                                ts.slack_d[i] = min(ts.t_d[i] - ts.WINDOWS[i].e, (ts.t_d[i] - (ts.tBest[i] - (ts.nRests[i] * ts.REST + (ts.nRests[i] - 1) * ts.DUTY))))
                                ts.remDuty_d[i] = ts.DUTY
                                ts.remDrive_d[i] = ts.DRIVE
                                # adjust previous
                                ts.t_d_shadow[i + 1] = ts.t_d[i+1] - ts.slack_a[i]
                                ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                        else:

                            print("Location: {}, Branch: {}".format(i, "F"))

                            ts.t_d[i] = ts.WINDOWS[i].l
                            ts.slack_d[i] = min(ts.t_d[i] - ts.WINDOWS[i].e, (ts.t_d[i] - (ts.tBest[i] - (ts.nRests[i]*ts.REST + (ts.nRests[i] - 1)*ts.DUTY))))
                            ts.remDuty_d[i] = ts.DUTY
                            ts.remDrive_d[i] = ts.DRIVE
                            # adjust previous
                            ts.t_d_shadow[i+1] = ts.t_d[i+1] - ts.slack_a[i]
                            ts.t_a_shadow[i] = ts.t_a[i] - ts.slack_a[i]

                    else:

                        print("Location: {}, Branch: {}".format(i, "E"))

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

                        print("Location: {}, Branch: {}".format(i, "C"))

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

                        # Branch D
                        print("Location: {}, Branch: {}".format(i, "D"))

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

    assert j > i

    #p = ts.nRests[i:(j+1)].index(1)
    #q = ts.nRests_between[i:(j+1)].index(1)

    p = smallest_nonzero(ts.nRests[i:(j + 1)])
    q = smallest_nonzero(ts.nRests_between[i:(j + 1)])

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
            ts.rest_push_end.append(j)

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




