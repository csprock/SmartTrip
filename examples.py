from utils import TimeWindow

# Author's Example
class AuthorsExample:

    WINDOWS = (TimeWindow(10, 15),
               TimeWindow(3, 18),
               TimeWindow(10, 18),
               TimeWindow(15, 35),
               TimeWindow(40, 45),
               TimeWindow(75, 100),
               TimeWindow(75, 100))

    travel_times = (6,2,4,10,10,15)