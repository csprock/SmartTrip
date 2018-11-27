from utils import TimeWindow, TripInterval, TripStats
from tsp import backwards_search, restore, smart_trip, compute_arrival_time, compute_nrests_between, push_up_nearest_rest, smallest_nonzero


# WINDOWS = (TimeWindow(10,15), TimeWindow(3,18), TimeWindow(10,18), TimeWindow(15,35), TimeWindow(40,45), TimeWindow(75, 100), TimeWindow(75,100))
# travel_times = (6,2,4,10,10,15)
# TS = TripStats(WINDOWS, travel_times)
#
# # WINDOWS = (TimeWindow(2,25),
# #            TimeWindow(10, 16),
# #            TimeWindow(1, 24),
# #            TimeWindow(33,33))
# # travel_times = (4, 4, 5)
# # #
# # TS = TripStats(WINDOWS, travel_times)
#
# #
# # WINDOWS = (TimeWindow(2, 10),
# #            TimeWindow(5, 10),
# #            TimeWindow(40,40))
# # travel_times = (5, 10)
# #
# # TS = TripStats(WINDOWS, travel_times)
#
# # WINDOWS = (TimeWindow(1, 10),
# #            TimeWindow(5, 10),
# #            TimeWindow(40,40))
# # travel_times = (9, 10)
# #
# # TS = TripStats(WINDOWS, travel_times)
#
# # WINDOWS = (TimeWindow(0,10), TimeWindow(5,9), TimeWindow(40,40))
# #
# # travel_times = (9,10)
# #
# # TS = TripStats(WINDOWS, travel_times)
#
# # WINDOWS = tuple(reversed((TimeWindow(100,100),
# #            TimeWindow(70,70),
# #            TimeWindow(61,70),
# #            TimeWindow(50,53),
# #            TimeWindow(20,20),
# #            TimeWindow(11,20))))
# #
# # travel_times = (9,10,1,9,10)
# #
# # TS = TripStats(WINDOWS, travel_times)
#
# print(TS.N_STOPS)
# #_, ts = smart_trip(TS)
# temp = smart_trip(TS)
# construct_trip(temp[1])

#temp = backwards_search(TS, 1, 0)
#temp = restore(temp[2], 3)
# temp = backwards_search(temp[1], 2, 0)
# temp = restore(temp[2], 0)

# temp[1].print_report()
