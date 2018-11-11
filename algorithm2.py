import math
from utils import TW

DRIVE = 11
DUTY = 14
REST = 10

WINDOWS = (TW(10,15), TW(3,18), TW(10,18), TW(15,35), TW(40,45), TW(75, 100), TW(75,100))
T = (6,2,4,10,10,15)

nRests_between = [None]*len(T)
nRests = [None]*(len(T) + 1)
remDrive_a = [None]*(len(T) + 1)
remDrive_d = [None]*(len(T) + 1)
remDuty_a = [None]*(len(T) + 1)
remDuty_d = [None]*(len(T) + 1)
t_a = [None]*(len(T) + 1)
t_d = [None]*(len(T) + 1)
slack_a = [None]*(len(T) + 1)
slack_d = [None]*(len(T) + 1)
wait = [None]*(len(T) + 1)
tBest = [None]*(len(T) + 1)

def print_report(i):

    arrive_message = '''
    Arrival: t: {}, slack: {}, remDrive: {}, remDuty: {}
    '''.format(t_a[i], slack_a[i], remDrive_a[i], remDuty_a[i])

    depart_message = '''
    Depart: tBest: {}, t: {}, slack: {}, remDrive: {}, remDuty: {}, wait: {}
    '''.format(tBest[i], t_d[i], slack_d[i], remDrive_d[i], remDuty_d[i], wait[i])

    print(arrive_message)
    print(depart_message)
    print('------')


# initialize
t_d[-1] = WINDOWS[-1].l
slack_d[-1] = WINDOWS[-1].delta
remDrive_d[-1] = 11
remDuty_d[-1] = 14

def run():
    for i in reversed(range(0,6)):
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
            print("Branch: A")
            return i
        else:

            if WINDOWS[i].e <= t_a[i] <= WINDOWS[i].l:
                slack_d[i] = min(slack_a[i], t_a[i] - WINDOWS[i].e)
                t_d[i] = t_a[i]
                remDrive_d[i] = remDrive_a[i]
                remDuty_d[i] = remDuty_a[i]

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
                                return i
                            else:
                                t_d[i] = t_a[i] - REST
                                slack_d[i] = min(t_d[i] - WINDOWS[i].l, (tBest[i] - (nRests[i] * REST + (nRests[i] - 1) * DUTY)))
                                remDuty_d[i] = DUTY
                                remDrive_d[i] = DRIVE
                                # adjust previous
                                t_d[i + 1] -= slack_a[i]
                        else:
                            t_d[i] = WINDOWS[i].l
                            slack_d[i] = min(t_d[i] - WINDOWS[i].l, (tBest[i] - (nRests[i]*REST + (nRests[i] - 1)*DUTY)))
                            remDuty_d[i] = DUTY
                            remDrive_d[i] = DRIVE
                            # adjust previous
                            t_d[i+1] -= slack_a[i]

                    else:
                        # adjust previous departure time
                        t_d[i+1] -= slack_a[i]
                        t_d[i] = WINDOWS[i].l
                        remDuty_d[i] = DUTY - ((tBest[i] - (nRests[i]*REST + (nRests[i] - 1)*DUTY)) - WINDOWS[i].l)
                        remDrive_d[i] = min(remDuty_d[i], DRIVE)
                        slack_d[i] = 0

                else:
                    wait[i] = t_a[i] - WINDOWS[i].l

                    # TODO: worked, check algo
                    if wait[i] > slack_a[i]:
                        # adjust previous departure time
                        t_d[i+1] -= slack_a[i]
                        slack_d[i] = 0
                        remDuty_d[i] = remDuty_a[i] - (wait[i] - slack_a[i])#- wait[i] - slack_a[i]
                        remDrive_d[i] = min(remDrive_a[i], remDuty_d[i])
                        t_d[i] = WINDOWS[i].l

                        print("Branch: C")
                        print_report(i)

                    else:
                        slack_d[i] = min(slack_a[i] - wait[i], WINDOWS[i].delta)
                        # adjust previous departure time
                        t_d[i+1] -= slack_a[i]
                        remDuty_d[i] = remDuty_a[i]
                        remDrive_d[i] = remDrive_a[i]
                        t_d[i] = WINDOWS[i].l

                        print("Branch: D")
                        print_report(i)
    print("yay!!!")

run()

print(t_a)
print(t_d)
