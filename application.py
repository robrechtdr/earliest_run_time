cnf = """30 1 /bin/run_me_daily
45 * /bin/run_me_hourly
* * /bin/run_me_every_minute
* 19 /bin/run_me_sixty_times"""

current_time = "16:10"







class CurrentTime(object):
    def __init__(self, cur_time):
        cur_time_spl = cur_time.split(":")
        self.hour = cur_time_spl[0]
        self.minute = cur_time_spl[1]


class CronLineTime(object):
    def __init__(self, cr_line):
        cr_line_spl = cr_line.split()
        self.path = cr_line_spl[2]
        self.hour = cr_line_spl[1]
        self.minute = cr_line_spl[0]


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
            rel_day = 1
        else:
            new_hour = str(int(hour) + 1)
            day_incr = 0
        return new_hour, day_incr

    # Not necessary as we don't count seconds and don't incr when same
    # minute and same hour.
    '''
    def incr_minute(minute):
        if minute == "59":
            new_minute = "00"
            hour_incr = 1
        else:
            new_minute = str(int(minute) + 1)
            hour_incr = 0
        return new_minute, hour_incr
    '''

    if cr_time.hour == "*":
        # E.g. cur_time; 23:10
        #       cr_time;  *:*
        # =>             23:10, today
        if cr_time.minute == "*":
            earl_hour = cur_time.hour
            earl_minute = cur_time.minute
            earl_day_ = 0
            return earl_hour, earl_minute, earl_day_
        else:
            # If cron minute alr in past
            # E.g. cur_time; 23:10
            #       cr_time;  *:05
            # =>             00:05, tomor
            #
            # E.g. cur_time; 22:10
            #       cr_time;  *:05
            # =>             23:05, today
            if cr_time.minute < cur_time.minute:
                earl_hour, earl_day_ = incr_hour(cur_time.minute)
                earl_minute = cr_time.minute
                # Could also have put the 'return' at the end but preferring
                # using returns immediately as it saves devs from having
                # to look at the condition and then further down as we
                # know returns exit the function.
                return earl_hour, earl_minute, earl_day_


            # Same as *:* , cr
            #
            # E.g. cur_time; 23:11
            #       cr_time;  *:11
            # =>             23:11, today
            else:
                earl_hour = cur_time.hour
                earl_minute = cr_time.minute
                earl_day_ = 0
                return earl_hour, earl_minute, earl_day_

    else:
        if cr_time.minute == "*":
            # Not same as *:* as takes minute from cur
            #
            # E.g. cur_time; 23:11
            #       cr_time; 22:*
            # =>             22:00, tomorrow
            if cr_time.hour < cur_time.hour:
                earl_hour = cr_time.hour
                earl_minute = "00"
                earl_day_ = 1
                return earl_hour, earl_minute, earl_day_

            else:
                # E.g. cur_time; 23:11
                #       cr_time; 24:*
                # =>             24:00, today
                earl_hour = cr_time.hour
                earl_minute = "00"
                earl_day_ = 0
                return earl_hour, earl_minute, earl_day_

        # If not * as minute nor as hour
        else:
            if cr_time.minute < cur_time.minute:
                # E.g. cur_time; 23:11
                #       cr_time; 22:10
                # =>             22:10, tomorrow
                if cr_time.hour < cur_time.hour:
                    earl_hour = cr_time.hour
                    earl_minute = cr_time.minute
                    earl_day_ = 1
                    return earl_hour, earl_minute, earl_day_

                # E.g. cur_time; 22:11
                #       cr_time; 23:10
                # =>             23:10, today
                else:
                    earl_hour = cr_time.hour
                    earl_minute = cr_time.minute
                    earl_day_ = 0
                    return earl_hour, earl_minute, earl_day_

            else:
                # E.g. cur_time; 23:11
                #       cr_time; 22:12
                # =>             22:12, tomorrow
                if cr_time.hour < cur_time.hour:
                    earl_hour = cr_time.hour
                    earl_minute = cr_time.minute
                    earl_day_ = 1
                    return earl_hour, earl_minute, earl_day_

                # E.g. cur_time; 22:11
                #       cr_time; 23:12
                # =>             23:12, today
                else:
                    earl_hour = cr_time.hour
                    earl_minute = cr_time.minute
                    earl_day_ = 0
                    return earl_hour, earl_minute, earl_day_


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


# Assuming that we can't use an already implemented cron lib : )
def main(current_time, cnf):
    """
    """

    '''
    #def resolve_abstractions# get_explicit_earliest_cr_time(self, cur_time):
    def get_earliest_run(self, cr_time, cur_time):
    def get_explicit_earliest_cr_time(cr_time, cur_time):
    # Prob best to calc earliest run time first and then say if tomorrow or not
    def _get_earliest_run(self, cr_time, cur_time):
    '''


    # get first line of cron
    #cronl = cnf.split("\n")[0]
    #cr_line = "30 1 /bin/run_me_daily"
    #cr_line = "45 * /bin/run_me_hourly"
    cr_time = CronLineTime(cr_line)
    cur_time = CurrentTime(current_time)

    earliest_run = get_earliest_run_time_prettified(cr_time, cur_time)
    #earliest_run = get_earliest_run(cr_time, cur_time)
    import pdb; pdb.set_trace()
    line_outp = earliest_run


if __name__ == "__main__":
    main(current_time, cnf)


