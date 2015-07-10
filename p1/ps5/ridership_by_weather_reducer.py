import sys
import logging

# from util import reducer_logfile
# logging.basicConfig(filename=reducer_logfile, format='%(message)s',
#                     level=logging.INFO, filemode='w')

# RUN:
# > cat ../ps4/turnstile_data_master_with_weather.csv | python ridership_by_weather_mapper.py | sort | python ridership_by_weather_reducer.py
# fog-norain	1315.57980681
# fog-rain	1115.13151799
# nofog-norain	1078.54679697
# nofog-rain	1098.95330076

def reducer():
    '''
    Given the output of the mapper for this assignment, the reducer should
    print one row per weather type, along with the average value of
    ENTRIESn_hourly for that weather type, separated by a tab. You can assume
    that the input to the reducer will be sorted by weather type, such that all
    entries corresponding to a given weather type will be grouped together.

    In order to compute the average value of ENTRIESn_hourly, you'll need to
    keep track of both the total riders per weather type and the number of
    hours with that weather type. That's why we've initialized the variable 
    riders and num_hours below. Feel free to use a different data structure in 
    your solution, though.

    An example output row might look like this:
    'fog-norain\t1105.32467557'

    Since you are printing the output of your program, printing a debug 
    statement will interfere with the operation of the grader. Instead, 
    use the logging module, which we've configured to log to a file printed 
    when you click "Test Run". For example:
    logging.info("My debugging message")
    Note that, unlike print, logging.info will take only a single argument.
    So logging.info("my message") will work, but logging.info("my","message") will not.
    '''

    riders = 0      # The number of total riders for this key
    num_hours = 0   # The number of hours with this key
    old_key = None

    def print_key():
        if old_key is not None:
            avg = 1.0 * riders / num_hours
            print '{0}\t{1}'.format(old_key, avg)


    for line in sys.stdin:
        key, new_riders = line.split('\t')
        if key != old_key:
            print_key()
            riders = 0
            num_hours = 0

        old_key = key
        riders = riders + float(new_riders)
        num_hours = num_hours + 1

    print_key()

reducer()

