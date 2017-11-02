import pytest
import unittest

from application import (get_earliest_run_time,
                         get_earliest_run_time_prettified,
                         CurrentTime, CronLineTime)


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Amount of test cases are proportional to the complexity (~likeliness
    # to cause problems) of the functions.
    def test_get_earliest_run_time(self):
        # Could define in setUp as well, negligeable benefit from doing so.
        cur_time = CurrentTime("16:10")

        cr_time = CronLineTime("30 1 /bin/run_me_daily")
        assert get_earliest_run_time(cr_time, cur_time) == ("1", "30", 1)

        # For a production system I might opt for a separate test for
        # each assert vs a test per function approach.
        # While quicker to write and simpler in structure this now only shows
        # the first assert that fails if multiple fail within the same test.
        #
        # Case C1
        cr_time = CronLineTime("45 * /bin/run_me_hourly")
        assert get_earliest_run_time(cr_time, cur_time) == ("16", "45", 0)

        # Case A
        cr_time = CronLineTime("* * /bin/run_me_every_minute")
        assert get_earliest_run_time(cr_time, cur_time) == ("16", "10", 0)

        # Case E
        cr_time = CronLineTime("* 19 /bin/run_me_sixty_times")
        assert get_earliest_run_time(cr_time, cur_time) == ("19", "00", 0)


        # Additional checks ######
        # Case B
        cur_time = CurrentTime("17:50")
        cr_time = CronLineTime("45 * /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("18", "45", 0)

        # Case C2
        cur_time = CurrentTime("17:45")
        cr_time = CronLineTime("45 * /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("17", "45", 0)

        # Case D
        cur_time = CurrentTime("20:29")
        cr_time = CronLineTime("* 19 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("19", "00", 1)

        # case F
        cur_time = CurrentTime("19:29")
        cr_time = CronLineTime("* 19 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("19", "29", 0)

        # Case G1
        cur_time = CurrentTime("1:31")
        cr_time = CronLineTime("30 0 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("0", "30", 1)

        # Case G2
        cur_time = CurrentTime("1:31")
        cr_time = CronLineTime("30 1 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("1", "30", 1)

        # Case H
        cur_time = CurrentTime("0:30")
        cr_time = CronLineTime("30 1 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("1", "30", 0)

        # Case I1
        cur_time = CurrentTime("2:29")
        cr_time = CronLineTime("30 1 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("1", "30", 1)

        # Case I2
        cur_time = CurrentTime("2:30")
        cr_time = CronLineTime("30 1 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("1", "30", 1)

        # Case J
        cur_time = CurrentTime("1:30")
        cr_time = CronLineTime("31 1 /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("1", "31", 0)

        # This case covers 23 hours incr to 0 with day incr
        cur_time = CurrentTime("23:10")
        cr_time = CronLineTime("05 * /bin/run_me_x")
        assert get_earliest_run_time(cr_time, cur_time) == ("0", "05", 1)


    def test_get_earliest_run_time_prettified(self):
        cur_time = CurrentTime("16:10")

        cr_time = CronLineTime("30 1 /bin/run_me_daily")
        assert get_earliest_run_time_prettified(cr_time, cur_time) == (
            "1:30 tomorrow - /bin/run_me_daily")

        cr_time = CronLineTime("* 19 /bin/run_me_sixty_times")
        assert get_earliest_run_time_prettified(cr_time, cur_time) == (
            "19:00 today - /bin/run_me_sixty_times")


if __name__ == "__main__":
    unittest.main()
