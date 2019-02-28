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


class ExampleA:

    WINDOWS = (TimeWindow(11, 20),
               TimeWindow(20, 20),
               TimeWindow(50, 53),
               TimeWindow(61, 70),
               TimeWindow(70, 70),
               TimeWindow(100, 100))

    travel_times = (9, 10, 1, 9, 10)

class ImpossibleExampleA:

    WINDOWS = (TimeWindow(9, 10),
               TimeWindow(10, 11),
               TimeWindow(11, 12))

    travel_times = (10, 0.5)