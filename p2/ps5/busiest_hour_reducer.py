import sys
import logging

# from util import reducer_logfile
# logging.basicConfig(filename=reducer_logfile, format='%(message)s',
#                     level=logging.INFO, filemode='w')

# RUN:
# >  cat ../ps4/turnstile_data_master_with_weather.csv | python busiest_hour_mapper.py | sort | python busiest_hour_reducer.py


def reducer():
    '''
    Write a reducer that will compute the busiest date and time (that is, the 
    date and time with the most entries) for each turnstile unit. Ties should 
    be broken in favor of datetimes that are later on in the month of May. You 
    may assume that the contents of the reducer will be sorted so that all entries 
    corresponding to a given UNIT will be grouped together.
    
    The reducer should print its output with the UNIT name, the datetime (which 
    is the DATEn followed by the TIMEn column, separated by a single space), and 
    the number of entries at this datetime, separated by tabs.

    For example, the output of the reducer should look like this:
    R001    2011-05-11 17:00:00	   31213.0
    R002	2011-05-12 21:00:00	   4295.0
    R003	2011-05-05 12:00:00	   995.0
    R004	2011-05-12 12:00:00	   2318.0
    R005	2011-05-10 12:00:00	   2705.0
    R006	2011-05-25 12:00:00	   2784.0
    R007	2011-05-10 12:00:00	   1763.0
    R008	2011-05-12 12:00:00	   1724.0
    R009	2011-05-05 12:00:00	   1230.0
    R010	2011-05-09 18:00:00	   30916.0
    ...
    ...

    Since you are printing the output of your program, printing a debug 
    statement will interfere with the operation of the grader. Instead, 
    use the logging module, which we've configured to log to a file printed 
    when you click "Test Run". For example:
    logging.info("My debugging message")
    Note that, unlike print, logging.info will take only a single argument.
    So logging.info("my message") will work, but logging.info("my","message") will not.
    '''

    max_entries = 0
    old_key = None
    datetime = ''

    def print_key():
        if old_key is not None:
            print '{0}\t{1}\t{2}'.format(old_key, datetime, max_entries)

    for line in sys.stdin:
        # remove the '\n' at the end of line
        key, entriesstr, date, time = line[:-1].split('\t')
        if key != old_key:
            print_key()
            max_entries = 0
            datetime = ''

        old_key = key
        entries = float(entriesstr)
        new_datetime = '{0} {1}'.format(date, time)
        if entries > max_entries or (entries == max_entries and new_datetime > datetime):
            max_entries = entries
            datetime = new_datetime
    # print the last key also
    print_key()

reducer()


