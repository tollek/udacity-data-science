from pandas import *
from ggplot import *
import pandasql
import numpy
import random
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def entries_per_hour_and_rain(turnstile_weather):
    grouped = turnstile_weather.groupby(['Hour', 'rain'])
    stats = grouped['ENTRIESn_hourly'].agg([numpy.sum, numpy.mean, numpy.std])
    # print stats
    stats = stats.reset_index()

    # Optionally, use geom_area(alpha=0.5) instaed of geom_point + geom_line
    gg = ggplot(aes(x='Hour', y='mean', color='rain'), data=stats) \
         + geom_point() \
         + geom_line() \
         + ggtitle('Subway Entries per hour') \
         + xlab('Hour') \
         + ylab('Entries mean')
    return gg


def entries_hourly_histogram(turnstile_weather):
    df_no_outliers = turnstile_weather[(turnstile_weather['ENTRIESn_hourly'] < 4995)]

    gg = ggplot(aes(x='ENTRIESn_hourly', fill='rain'), data=df_no_outliers) \
         + geom_histogram(aes(alpha=0.5, position='dodge', binwidth=150)) \
         + ggtitle('Subway Entries per hour') \
         + xlab('# of entries per hour [ENTRIESn_hourly]') \
         + ylab('count')
    #print gg
    return gg


def weekday_hour(df_row):
    pd = datetime.datetime.strptime(df_row['DATEn'], '%Y-%m-%d')
    return pd.strftime("%a") + '_{:02d}'.format(df_row['Hour'] / 3 * 3)
    #return (pd.weekday() * 24 + df_row['Hour']) / 3 * 3


def index_key(df, idx):
    base = {
        "Mon": 1,
        "Tue": 2,
        "Wed": 3,
        "Thu": 4,
        "Fri": 5,
        "Sat": 6,
        "Sun": 7
    }
    v = df.iloc[idx]['weekday_hour']
    return base[v[:3]] * 24 + int(v[4:])


def entries_hourly_throughout_week(turnstile_weather):
    pandas.options.mode.chained_assignment
    turnstile_weather.is_copy = False
    # grouped = turnstile_weather.groupby(['DATEn', 'Hour', 'rain'])
    turnstile_weather['weekday_hour'] = turnstile_weather.apply(weekday_hour, axis=1)
    grouped = turnstile_weather.groupby(['weekday_hour'])
    grouped = grouped['ENTRIESn_hourly'].agg([len, numpy.mean, numpy.median], axis=0)
    grouped = grouped.reset_index()

    # Reorder the data so that Monday is first
    index = sorted(grouped.index, key=lambda x: index_key(grouped, x))
    grouped = grouped.reindex(index)

    gg = ggplot(aes(x='weekday_hour', y='mean'), data=grouped) \
        + geom_bar(stat='identity') \
        + ggtitle('Subway Entries per day and hour') \
        + xlab('Hour and Day of week') \
        + ylab('Mean # of entries') \
        + theme(axis_text_x  = element_text(angle = 90, hjust = 0.4))
    return gg


def plot_weather_data(turnstile_weather):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.

    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning
    ridership and time of day in exercise #1, maybe look at weather and try to make a
    histogram in this exercise). Or try to use multiple encodings in your graph if
    you didn't in the previous exercise.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

   However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    plot = entries_per_hour_and_rain(turnstile_weather)
    # plot = entries_hourly_histogram(turnstile_weather)
    # plot = entries_hourly_throughout_week(turnstile_weather)
    return plot


def main():
    df = pandas.read_csv('turnstile_data_master_with_weather.csv')
    plot = plot_weather_data(df)
    print(plot)

if __name__ == "__main__":
    main()


