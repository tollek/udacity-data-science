# NOTE(tollek): this code has been written as an implementation of Data Science nanodegree.
# In older version of the course, one of the excercises was to implement the gradient descent
# on my own (instead of using scikit.SGDRegressor. 
# Here is the solutions - although not merged into linear_regression.py, to simplify the review process.
#
# Nice part about this implementation of gradient_descent is the history of cost function - decreasing
# over time with iterations of gradient descent.
import numpy
import pandas

def compute_cost(features, values, theta):
    """
    Compute the cost of a list of parameters, theta, given a list of features 
    (input data points) and values (output data points).
    """
    m = len(values)
    sum_of_square_errors = numpy.square(numpy.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    """

    # Write code here that performs num_iterations updates to the elements of theta.
    # times. Every time you compute the cost for a given list of thetas, append it 
    # to cost_history.
    # See the Instructor notes for hints. 

    cost_history = []

    ###########################
    ### YOUR CODE GOES HERE ###
    ###########################
    m = len(features)
    cost_history = []

    for i in xrange(num_iterations):
        # h is vector of predicted values
        h = numpy.dot(features, theta)
        # numpy.dot(h - values, features) ==> partial derivative of J(theta)
        theta_update = -alpha / m * numpy.dot(h - values, features)
        theta = theta + theta_update
        cost = compute_cost(features, values, theta)
        cost_history.append(cost)

    return theta, pandas.Series(cost_history) # leave this line for the grader
