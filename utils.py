
class TripInterval:

    def __init__(self, type, start, end):

        assert type in ['rest', 'duty', 'drive']

        self.type = type
        self.start = start
        self.end = end
        self.duration = end - start


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


class TimeWindow:

    def __init__(self, e, l):
        
        assert l > e

        self.e = e
        self.l = l
        self.delta = l - e
