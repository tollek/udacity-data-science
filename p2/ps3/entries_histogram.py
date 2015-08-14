import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histograph may look similar to bar graph in the instructor notes below.
    
    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''

    tw = turnstile_weather
    bins = 30
    outlier_cut = 5000

    sunny_hist = tw[(tw['rain'] == 0.0) & (tw['ENTRIESn_hourly'] <= outlier_cut)]
    rain_hist = tw[(tw['rain'] == 1.0) & (tw['ENTRIESn_hourly'] <= outlier_cut)]

    outliers_n = len(tw[tw['ENTRIESn_hourly'] > outlier_cut])
    print 'removed outliers %d / %d (%f)' % (outliers_n, len(tw), 1.0 * outliers_n / len(tw))

    # Histogram of entries (not normalized)
    plt.hist((sunny_hist['ENTRIESn_hourly'].tolist(), rain_hist['ENTRIESn_hourly'].tolist()),
             label = ['no rain', 'rain'], bins = bins, normed=False)
    plt.title('Subway ENTRIES population [outliers excluded]')
    plt.xlabel('ENTRIESn_hourly')
    plt.ylabel('Count')
    plt.legend(loc='upper right')
    plt.savefig('histogram_subway_entries_distribution.png')
    plt.show()
    plt.close()
    # Comment-out the plt.close above and uncomment the return for udacity test run.
    # return plt

    # Histogram of entries (normalized)
    plt.hist((sunny_hist['ENTRIESn_hourly'].tolist(), rain_hist['ENTRIESn_hourly'].tolist()),
             label = ['no rain', 'rain'], bins = bins, normed=True)
    plt.title('Normalized subway ENTRIES population [outliers excluded]')
    plt.xlabel('ENTRIESn_hourly')
    plt.ylabel('Normalized count')
    plt.legend(loc='upper right')
    plt.savefig('histogram_subway_entries_distribution_normalized.png')
    plt.show()
    plt.close()
    return None


turnstile_weather = pandas.read_csv('turnstile_data_master_with_weather.csv')
entries_histogram(turnstile_weather)

