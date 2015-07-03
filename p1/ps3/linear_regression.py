import datetime
import numpy as np
import pandas
import sklearn.linear_model as scikit
import statsmodels.api as sm
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


def add_columns(df):
    '''
    Adds new categorical features to dataframe:
        - UNIT
        - day_of_week
    '''
    date_values = {}
    for d in df['DATEn'].unique():
        pd = datetime.datetime.strptime(d, '%Y-%m-%d')
        date_values[d] = pd.weekday()

    df['day_of_week'] = df.apply(lambda x: date_values[x['DATEn']], axis=1)
    df['weekend'] = df.apply(lambda x: date_values[x['DATEn']] >= 5, axis=1)
    df['bank_holiday'] = df.apply(lambda x: x['DATEn'] == '2011-05-30', axis=1) # Memorial Day


def linear_regression_ols(features, values):
    """
    Performs linear regression using OLS (ordinary least squared method).

    Returns the intercept and the parameters, that is, the optimal values of theta.

    This page contains example code that may be helpful:
    http://statsmodels.sourceforge.net/0.5.0/generated/statsmodels.regression.linear_model.OLS.html
    """

    features = sm.add_constant(features)
    model = sm.OLS(values, features)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    return intercept, params


def normalize_features(features):
    ''' 
    Returns the means and standard deviations of the given features, along with a normalized feature
    matrix.
    '''
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    ''' 
    Recovers the weights for a linear model given parameters that were fitted using
    normalized features. Takes the means and standard deviations of the original
    features, along with the intercept and parameters computed using the normalized
    features, and returns the intercept and parameters that correspond to the original
    features.
    '''
    # NOTE(pawelb): my intuition behind the transformation
    # params: norm_params have values such that normalized_features * norm_params = values
    #   now, as we de-normalize features (use the original values), we effectively have:
    #       1. normalized_features * norm_params = values
    #       2.  features * params = values
    #       1. && 2. =>
    #          normalized_features * norm_params = features * params
    #          features / std_devs * norm_params = features * params
    #                   1/std_devs * norm_params = params
    #                                     params = norm_params / std_devs
    #
    #   intercept:
    #        - np.sum(means * norm_params / std_devs) - is basically recovering all the means back
    #        - we take -(norm_intercept - np.sum(means * norm_params / std_devs)) which is transposition (?) of chart
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression_gradient(features, values):
    """
    Perform linear regression using gradient descent method.
    """
    means, std_devs, normalized_features_array = normalize_features(features)

    clf = scikit.SGDRegressor(alpha=0.1, n_iter=25)
    clf.fit(normalized_features_array, values)
    norm_intercept, norm_params = clf.intercept_, clf.coef_

    intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
    return intercept, params


def plot_residuals(turnstile_weather, predictions):
    '''
    Plots histogram of the residuals = the difference between the original hourly entry data and the predicted values

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''

    plt.figure()
    errs = turnstile_weather['ENTRIESn_hourly'] - predictions
    plt.hist(errs.tolist(), bins=50)
    plt.show()
    return plt


def compute_r_squared(data, predictions):
    # returns the coefficient of determination, R^2
    n = len(data)
    prediction_error = sum((data - predictions)**2)
    data_mean = np.mean(data)
    data_var = sum((data - np.repeat(data_mean, n))**2)
    r_squared = 1.0 - 1.0 * prediction_error / data_var
    return r_squared


def predictions(dataframe):
    '''
    Creates linear regression model predicting ENTRIESn_hourly and evaluates it's performance
    (plot residuals & compute R^2).

    Either OLS or gradient descent method is used.
    '''

    add_columns(dataframe)

    # add/remove features by uncommenting/commenting feature names
    weather_features_names = [
        # 'maxpressurei',
        # 'maxdewpti',
        # 'mindewpti',
        # 'minpressurei',
        # 'meandewpti',
        # 'meanpressurei',
        # 'fog',
        'rain',
        # 'meanwindspdi',
        # 'mintempi',
        # 'meantempi',
        # 'maxtempi',
        # 'precipi',
    ]
    features = dataframe[weather_features_names]

    # add/remove categoric features by removing dummies for given feature
    #print len(features.columns)
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    #print len(features.columns)
    dummy_units = pandas.get_dummies(dataframe['Hour'], prefix='hour')
    features = features.join(dummy_units)
    #print len(features.columns)
    dummy_units = pandas.get_dummies(dataframe['day_of_week'], prefix='day_of_week')
    features = features.join(dummy_units)
    #print len(features.columns)

    # Values
    values = dataframe['ENTRIESn_hourly']
    # Get numpy arrays
    features_array = features.values
    values_array = values.values

    # NOTE(pawelb):
    # gradient R^2 (udacity data) = .470
    # OLS R^2 = .536
    # Perform gradient descent
    #  intercept, params = linear_regression_gradient(features.values, values_array)
    # alternatively, use OLS
    intercept, params = linear_regression_ols(features.values, values_array)
    print 'intercept: ', intercept
    for i, _ in enumerate(weather_features_names):
	    print weather_features_names[i], '\t\t', params[i]

    predictions = intercept + np.dot(features_array, params)

    # plot_residuals(dataframe, predictions)
    r_squared = compute_r_squared(values, predictions)
    print 'r_squared = ', r_squared

    return predictions


def main():
    turnstile_weather = pandas.read_csv('turnstile_data_master_with_weather.csv')
    turnstile_weather = turnstile_weather.sample(len(turnstile_weather) / 5, random_state = 7)
    p = predictions(turnstile_weather)
    print p

if __name__ == "__main__":
    main()
