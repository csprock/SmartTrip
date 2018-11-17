from array import array
import math
from utils import TW
from copy import copy

DRIVE = 11
DUTY = 14
REST = 10

WINDOWS = (TW(10,15), TW(3,18), TW(10,18), TW(15,35), TW(40,45), TW(75, 100), TW(75,100))
T = (6,2,4,10,10,15)

nRests_between = [0]*len(T)
nRests = [0]*(len(T) + 1)
remDrive_a = [None]*(len(T) + 1)
remDrive_d = [None]*(len(T) + 1)
remDuty_a = [None]*(len(T) + 1)
remDuty_d = [None]*(len(T) + 1)
t_a = [None]*(len(T) + 1)
t_d = [None]*(len(T) + 1)
slack_a = [None]*(len(T) + 1)
slack_d = [None]*(len(T) + 1)
wait = [0]*(len(T) + 1)
tBest = [None]*(len(T) + 1)

# declare "shadow" variables
t_a_shadow = [None]*(len(T) + 1)
t_d_shadow = [None]*(len(T) + 1)

rest_push_end = int()

def print_report(i):

    global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest


    arrive_message = '''
    At location {}: \n \t Arrival: t: {}, slack: {}, remDrive: {}, remDuty: {} \n \t Depart: tBest: {}, t: {}, slack: {}, remDrive: {}, remDuty: {}, wait: {}
    '''.format(i, t_a[i], slack_a[i], remDrive_a[i], remDuty_a[i], tBest[i], t_d[i], slack_d[i], remDrive_d[i], remDuty_d[i], wait[i])

    print(arrive_message)
    print('------')


# initialize
t_d[-1] = WINDOWS[-1].l
slack_d[-1] = WINDOWS[-1].delta
remDrive_d[-1] = 11
remDuty_d[-1] = 14

def backwards_search(k, j, debug=False):

    global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest

    for i in reversed(range(j, k+1)):
        print(i)
        # Phase I: compute arrival time
        if T[i] <= remDrive_d[i+1]:
            t_a[i] = t_d[i+1] - T[i]
            remDrive_a[i] = remDrive_d[i+1] - T[i]
            remDuty_a[i] = remDuty_a[i+1] - T[i]
            slack_a[i] = slack_d[i+1]
        else:
            nRests_between[i] = 1 + math.floor((T[i] - remDrive_d[i+1])/DRIVE)
            t_a[i] = t_d[i+1] - (T[i] + nRests_between[i]*REST)
            slack_a[i] = slack_d[i+1] + (remDuty_d[i+1] - remDrive_d[i+1]) + (nRests_between[i] - 1)*(DUTY - DRIVE)
            remDuty_a[i] = DUTY - ((T[i] - remDrive_d[i+1]) % DRIVE)
            remDrive_a[i] = DRIVE - ((T[i] - remDrive_d[i + 1]) % DRIVE)

        # Phase II: analyze arrival time
        if t_a[i] < WINDOWS[i].e:
            return False, i
        else:

            if WINDOWS[i].e <= t_a[i] <= WINDOWS[i].l:
                slack_d[i] = min(slack_a[i], t_a[i] - WINDOWS[i].e)
                t_d[i] = copy(t_a[i])
                remDrive_d[i] = remDrive_a[i]
                remDuty_d[i] = remDuty_a[i]


                if debug:
                    print("Branch: B")
                    print_report(i)


            else:
                tBest[i] = t_a[i] - slack_a[i] - remDuty_a[i]
                if tBest[i] > WINDOWS[i].l:

                    nRests[i] = math.ceil((tBest[i] - WINDOWS[i].l)/(DRIVE + DUTY))
                    wait[i] = max(t_a[i] - WINDOWS[i].l - nRests[i]*REST, 0)

                    if tBest[i] - (nRests[i]*REST + (nRests[i] - 1)*DUTY) < WINDOWS[i].l:

                        if t_a[i] - REST < WINDOWS[i].l:
                            if t_a[i] - REST < WINDOWS[i].l:
                                return False, i
                            else:
                                t_d[i] = t_a[i] - REST
                                slack_d[i] = min(t_d[i] - WINDOWS[i].l, (tBest[i] - (nRests[i] * REST + (nRests[i] - 1) * DUTY)))
                                remDuty_d[i] = DUTY
                                remDrive_d[i] = DRIVE
                                # adjust previous
                                t_d_shadow[i + 1] = t_d[i+1] - slack_a[i]
                                t_a_shadow[i] = t_a[i] - slack_a[i]
                        else:
                            t_d[i] = WINDOWS[i].l
                            slack_d[i] = min(t_d[i] - WINDOWS[i].l, (tBest[i] - (nRests[i]*REST + (nRests[i] - 1)*DUTY)))
                            remDuty_d[i] = DUTY
                            remDrive_d[i] = DRIVE
                            # adjust previous
                            t_d_shadow[i+1] = t_d[i+1] - slack_a[i]
                            t_a_shadow[i] = t_a[i] - slack_a[i]

                    else:
                        # adjust previous departure time
                        t_d_shadow[i+1] = t_d[i+1] - slack_a[i]
                        t_a_shadow[i] = t_a[i] - slack_a[i]

                        t_d[i] = WINDOWS[i].l
                        remDuty_d[i] = DUTY - ((tBest[i] - (nRests[i]*REST + (nRests[i] - 1)*DUTY)) - WINDOWS[i].l)
                        remDrive_d[i] = min(remDuty_d[i], DRIVE)
                        slack_d[i] = 0

                else:
                    wait[i] = t_a[i] - WINDOWS[i].l

                    # TODO: worked, check algo
                    if wait[i] > slack_a[i]:
                        # adjust previous departure time
                        t_d_shadow[i+1] = t_d[i+1] - slack_a[i]
                        t_a_shadow[i] = t_a[i] - slack_a[i]

                        slack_d[i] = 0
                        remDuty_d[i] = remDuty_a[i] - (wait[i] - slack_a[i])#- wait[i] - slack_a[i]
                        remDrive_d[i] = min(remDrive_a[i], remDuty_d[i])
                        t_d[i] = WINDOWS[i].l


                        if debug:
                            print("Branch: C")
                            print_report(i)

                    else:
                        slack_d[i] = min(slack_a[i] - wait[i], WINDOWS[i].delta)

                        # adjust previous departure time
                        t_d_shadow[i+1] = t_d[i+1] - slack_a[i]
                        t_a_shadow[i] = t_a[i] - slack_a[i]


                        remDuty_d[i] = remDuty_a[i]
                        remDrive_d[i] = remDrive_a[i]
                        t_d[i] = WINDOWS[i].l

                        if debug:
                            print("Branch: D")
                            print_report(i)
    return True, i




def compute_nrests_between(j, i):

    global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest

    assert j < i

    nrests_ijs = 0
    nrests_ijb = 0

    # count all rests at stops j through i
    for k in range(j, i+1):
        nrests_ijs += nRests[k]

    # count all rests between stops j and i
    # nRests_between[k] = rests taken between k and k+1
    for k in range(j, i):
        nrests_ijb += nRests_between[k]

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

def push_up_nearest_rest(i, j):

    global nRests, nRests_between

    assert j > i

    p = nRests[i:(j+1)].index(1)
    q = nRests_between[i:(j+1)].index(1)

    if p <= q:
        nRests[i + p] = 0
    else:
        nRests_between[i + q] = 0







def restore(i, debug=False):

    global nRests, nRests_between, remDuty_a, remDuty_d, remDrive_d, remDrive_a, t_a, t_d, slack_a, slack_d, wait, tBest, rest_push_end

    N = 6 # for testing only
    for j in range(i+1, N):

        nRests_ij, _ , _  = compute_nrests_between(i, j)
        #print("Rests between {} and {}: {}, waits at {}: {}".format(i,j, nRests_ij, j, wait[j]))

        if wait[j] > 0 and nRests_ij > 0:
            #print_report(j)
            nRests[j] += 1

            push_up_nearest_rest(i, j)
            rest_push_end = j
            print("Rest push end: {}".format(rest_push_end))



            if t_a[j] - nRests[j]*REST >= WINDOWS[j].e:

                if t_a[j] - (nRests[j]*REST) <= WINDOWS[j].l:
                    t_d[j] = t_a[j] - nRests[j]*REST
                    remDuty_d[j] = DUTY
                    remDrive_d[j] = DRIVE
                    wait[j] = 0
                    slack_d[j] = min(t_d[j]-WINDOWS[j].e, slack_a[j] + remDuty_a[j] + (nRests[j] - 1)*REST)

                    if debug:
                        print("In Branch B at location {}".format(j))
                        print_report(j)
                else:
                    t_d[j] = WINDOWS[j].l
                    remDuty_d[j] = DUTY
                    remDrive_d[j] = DRIVE
                    wait[j] = t_a[j] - nRests[j]*REST - WINDOWS[j].l
                    slack_d[j] = min(WINDOWS[j].delta, slack_a[j] + remDuty_a[j] + (nRests[j] -1)*REST - (t_a[j] - nRests[j]*REST - WINDOWS[j].l))

                    if debug:
                        print("In Branch A at location {}".format(j))
                        print_report(j)

            print("In backwards search from {} to {}".format(j-1, i))
            placeholder_i = backwards_search(j-1, i, debug=True)
            print("=========================")

            if t_a[i] >= WINDOWS[i].e:
                print("Done!!")
                return True

            else:
                nRests[j] -= 1

        else:
            continue

    return False


#
# def smart_trip():
#
#     Done = False
#
#     j = 5
#     while j > 0:
#         i = backwards_search(j, 0)
#         print(i)
#         # if i == 0:
#         #     return True
#         # else:
#         restore_status = restore(i)
#         print("restore called at {}".format(i))
#         if restore_status == True:
#             j = i - 1
#         else:
#             return False
#


results = backwards_search(5,0, debug = False)
#status = restore(0, debug = False)
#print(rest_push_end)
#print(nRests_between)

# TODO: combine shadow with actual

for i in range(rest_push_end + 1, 5):

    if t_a_shadow[i] and t_d_shadow[i+1]:
        t_a[i] = t_a_shadow[i]
        t_d[i+1] = t_d_shadow[i+1]


# construct path
# using nRests, t_d, t_a

legs = list()

T = t_d[6]

i = 5

if nRests_between[i] > 0:
    legs.append(('drive', T - remDrive_d[i + 1], T))

    T -= remDrive_d[i+1]
    for rests in range(nRests_between[i]):
        legs.append(('rest', T - 10, T))
        T -= 10
        print(T)
        legs.append(('drive', T - min(11, T - t_a[i]), T))
        T -= min(T, T - t_a[i])

else:
    legs.append(('drive', t_a[i], T))
    T -= T - t_a[i]

if nRests[i] > 0:
    legs.append(('rest', T - 10*nRests[i], T))
    T -= 10*nRests[i]
if t_d[i] < T:
    legs.append(('wait', T - (t_a[i] - t_d[i]), T))
    T -= t_a[i] - t_d[i]

i -= 1
print(legs)


