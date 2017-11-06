import sys


class CurrentTime(object):
    def __init__(self, cur_time):
        cur_time_spl = cur_time.split(":")
        self.hour = cur_time_spl[0]
        self.minute = cur_time_spl[1]

    def __repr__(self):
        return "CurrentTime('{0}:{1}')".format(self.hour, self.minute)


class CronLineTime(object):
    def __init__(self, cr_line):
        cr_line_spl = cr_line.split()
        self.path = cr_line_spl[2]
        self.hour = cr_line_spl[1]
        self.minute = cr_line_spl[0]

    def __repr__(self):
        return "CronLineTime('{0} {1} {2}')".format(self.minute, self.hour, self.path)


# Assuming that we can't use a cron parsing lib.
def get_earliest_run_time(cr_time, cur_time):
    """
    Output the soonest time at which each of the commands will fire
    and whether it is today (0) or tomorrow (1). In the case when the task
    should fire at the simulated 'current time' then that is the time you
    should output, not the next one.

    Returns:
        earliest_hour (str), earliest_minute (str), day_increment (int)

    E.g.
        cron time                                  : 45 *
        current_time                               : 16:10
        -------------
        earliest_run_time(cron_time, current_time) : 16:45, today (=0)

    >>> cr_time = CronLineTime("45 * /bin/run_me_hourly")
    >>> cur_time = CurrentTime("16:10")
    >>> earl_hour, earl_minute, day_incr = get_earliest_run_time(cr_time,
                                                                 cur_time)
    >>> earl_hour
    "16"
    >>> earl_minute
    "45"
    >>> day_incr
    0

    """
    earl_minute = None
    earl_hour = None
    earl_day = None

    def incr_hour(hour):
        """
        Returns hour and increment of the rel_day
        """
        if hour == "23":
            # As example output "1:30" seems to use a single digit for the hour.
            new_hour = "0"
            day_incr = 1
        else:
            new_hour = str(int(hour) + 1)
            day_incr = 0
        return new_hour, day_incr

    # Case A
    # E.g. cur_time; 23:10
    #       cr_time;  *:*
    # =>             23:10, today
    if cr_time.hour == "*" and cr_time.minute == "*":
        earl_hour = cur_time.hour
        earl_minute = cur_time.minute
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    # Case B
    # If cron minute alr in past
    # E.g. cur_time; 23:10
    #       cr_time;  *:05
    # =>             00:05, tomor
    #
    # E.g. cur_time; 22:10
    #       cr_time;  *:05
    # =>             23:05, today
    elif cr_time.hour == "*" and cr_time.minute < cur_time.minute:
        earl_hour, earl_day = incr_hour(cur_time.hour)
        earl_minute = cr_time.minute
        # Could also have put the 'return' at the end but preferring
        # using returns immediately as it saves devs from having
        # to look at the condition and then further down as we
        # know returns exit the function.
        return earl_hour, earl_minute, earl_day

    # Case C1
    # E.g. cur_time; 23:10
    #       cr_time;  *:11
    # =>             23:11, today
    #
    # Case C2
    # E.g. cur_time; 23:11
    #       cr_time;  *:11
    # =>             23:11, today
    elif cr_time.hour == "*" and cr_time.minute >= cur_time.minute:
        earl_hour = cur_time.hour
        earl_minute = cr_time.minute
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    # Case D
    # E.g. cur_time; 23:11
    #       cr_time; 22:*
    # =>             22:00, tomorrow
    elif cr_time.minute == "*" and cr_time.hour < cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = "00"
        earl_day = 1
        return earl_hour, earl_minute, earl_day

    # Case E
    # E.g. cur_time; 23:11
    #       cr_time; 24:*
    # =>             24:00, today
    elif cr_time.minute == "*" and cr_time.hour > cur_time.hour:
            earl_hour = cr_time.hour
            earl_minute = "00"
            earl_day = 0
            return earl_hour, earl_minute, earl_day

    # Case F
    # E.g. cur_time; 23:11
    #       cr_time; 24:*
    # =>             24:00, today
    elif cr_time.minute == "*" and cr_time.hour == cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = cur_time.minute
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    # Case D
    # E.g. cur_time; 23:11
    #       cr_time; 22:*
    # =>             22:00, tomorrow
    elif cr_time.minute == "*" and cr_time.hour < cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = "00"
        earl_day = 1
        return earl_hour, earl_minute, earl_day

    # Case E
    # E.g. cur_time; 23:11
    #       cr_time; 24:*
    # =>             24:00, today
    elif cr_time.minute == "*" and cr_time.hour > cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = "00"
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    # Case F
    # E.g. cur_time; 23:11
    #       cr_time; 24:*
    # =>             24:00, today
    elif cr_time.minute == "*" and cr_time.hour == cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = cur_time.minute
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    # Case G1
    # cr_time.hour == cur_time.hour
    # E.g. cur_time; 23:11
    #       cr_time; 22:11
    # =>             22:11, tomorrow
    #
    # Case G2
    # cr_time.hour < cur_time.hour
    # E.g. cur_time; 23:11
    #       cr_time; 22:10
    # =>             22:10, tomorrow
    #
    elif cr_time.minute < cur_time.minute and cr_time.hour <= cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = cr_time.minute
        earl_day = 1
        return earl_hour, earl_minute, earl_day

    # Case H
    # E.g. cur_time; 22:11
    #       cr_time; 23:10
    # =>             23:10, today
    elif cr_time.minute < cur_time.minute and cr_time.hour > cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = cr_time.minute
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    # Case I
    # E.g. cur_time; 23:11
    #       cr_time; 22:12
    # =>             22:12, tomorrow
    elif cr_time.minute >= cur_time.minute and cr_time.hour < cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = cr_time.minute
        earl_day = 1
        return earl_hour, earl_minute, earl_day

    # Case J
    # E.g. cur_time; 22:11
    #       cr_time; 23:12
    # =>             23:12, today
    elif cr_time.minute >= cur_time.minute and cr_time.hour >= cur_time.hour:
        earl_hour = cr_time.hour
        earl_minute = cr_time.minute
        earl_day = 0
        return earl_hour, earl_minute, earl_day

    else:
        # In case we'd run this application from another program and we'd need the 
        # exception to be caught, we can then use a custom exception here.
        raise ValueError("Unhandled case")


def get_earliest_run_time_prettified(cr_time, cur_time):
    """
    Get the prettified form of get_earliest_run_time.
    """
    earl_h, earl_m, earl_day_ = get_earliest_run_time(cr_time, cur_time)

    earl_day = None
    if earl_day_ == 0:
        earl_day = "today"
    elif earl_day_ == 1:
        earl_day = "tomorrow"

    earl_time_str = "{0}:{1} {2} - {3}".format(earl_h,
                                               earl_m,
                                               earl_day,
                                               cr_time.path)
    return earl_time_str


if __name__ == "__main__":
    current_time = sys.argv[1]
    cur_time = CurrentTime(current_time)

    # Using this instead of readlines to get rid of \n
    cronlines = [line.rstrip('\n') for line in sys.stdin]
    for cronline in cronlines:
        cr_time = CronLineTime(cronline)
        earliest_run_time = get_earliest_run_time_prettified(cr_time, cur_time)
        print earliest_run_time
