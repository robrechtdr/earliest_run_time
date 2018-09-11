## Problem

We have a set of tasks, each running at least daily, which are scheduled using some simple values in a text file. You might recognise this from writing a crontab configuration in the past.

Examples of the the scheduler config:

	30 1 /bin/run_me_daily
	45 * /bin/run_me_hourly
	* * /bin/run_me_every_minute
	* 19 /bin/run_me_sixty_times

The first field is the minute past the hour, the second field is the hour of the day and the third is the command to run. For both cases * means that it should run for all values of that field. In the above example run_me_daily has been set to run at 1:30am every day and run_me_hourly at 45 minutes past the hour every hour. The fields are whitespace separated and each entry is on a separate line.

We want you to write a command line program that takes a single argument. This argument is the simulated 'current time' in the format HH:MM. The program should accept config lines in the form above to STDIN and output the soonest time at which each of the commands will fire and whether it is today or tomorrow. In the case when the task should fire at the simulated 'current time' then that is the time you should output, not the next one.

For example given the above examples as input and the simulated 'current time' command-line argument 16:10 the output should be:

	1:30 tomorrow - /bin/run_me_daily
	16:45 today - /bin/run_me_hourly
	16:10 today - /bin/run_me_every_minute
	19:00 today - /bin/run_me_sixty_times

You can submit your solution in any language you like. Python, PHP, C, JavaScript, Go, Rust, Swift, Awk, Prolog. The choice is yours as long as we can run it as described below.

We will want to run your code, so please supply instructions for building and running it. Additionally, it must work on at least one of OS X or Linux.

We want to run your code on the command line using an input like

	./<your app> HH:MM < config

For example: `./application.py 16:10 < config`

Where ‘config’ is a file containing various cron style inputs like we described above.



## Solution

### Run

E.g. `python application.py 16:10 < config`

### Tests

* The program uses pytest for testing, so do the following before running them:    
    `pip install -r requirements.txt`

* To run the tests, execute the following:    
    `py.test tests.py -v`
