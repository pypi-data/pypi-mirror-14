""" Statistical functions and utilities. """
import numpy as np
from scipy.stats import describe
import pandas as pd
import math
from collections import namedtuple
from math import sqrt


def rss(actual, forecast):
    ''' Computes the residuals squares sum (RSS).

    .. math:: RSS = \sum_{i=1}^n (y_i - f(x_i))^2

    :param actual: The target values.
    :param forecast: Predicted values.

    :returns: The RSS.
    '''
    return ((actual - forecast) ** 2).sum()


def mse(actual, forecast):
    ''' Computes the mean squared error.

    .. math:: \operatorname{MSE}=\\frac{1}{n}\\sum_{i=1}^n(\\hat{Y_i} - Y_i)^2

    :param actual: The target values.
    :param forecast: Predicted values.

    :returns: The MSE.

    '''
    return ((actual - forecast) ** 2).mean()


def mpe(actual, forecast):
    ''' Computes the mean percentage error. \
        Non-finite values due to zero division are ignored.

    .. math:: \\text{MPE} = \\frac{100\\%}{n}\\sum_{t=1}^n \\frac{a_t-f_t}{a_t}

    :param actual: The target values.
    :param forecast: Predicted values.

    :returns: The MPE.
    '''
    ratio = (actual - forecast)/actual
    ratio = ratio[np.isfinite(ratio)]

    return 100 * ratio.mean()


def mape(actual, forecast):
    ''' Computes the mean absolute percentage error. \
        Non-finite values due to zero division are ignored.

    .. math::  \mbox{MAPE} = \\frac{1}{n}\\sum_{t=1}^n  \
        \\left|\\frac{A_t-F_t}{A_t}\\right|

    :param actual: The target values.
    :param forecast: Predicted values.

    :returns: The MAPE.
    '''
    ratio = (actual - forecast)/actual
    ratio = ratio[np.isfinite(ratio)]

    return np.abs(ratio).mean()


def wssse(point, center):
    ''' Computes the **Within Set Sum of Squared Error(WSSSE)**.

    :param point: A point for which to calculate the error.
    :param center: The center of a cluster.

    :returns: The WSSSE.
    '''
    return sqrt(sum([x**2 for x in (point - center)]))


def trimean(arr):
    """ Calculates the trimean.

    .. math:: TM=\\frac{Q_1 + 2Q_2 + Q_3}{4}

    :param arr: An array containing numbers.

    :returns: The trimean for the array.

    >>> import numpy as np
    >>> from dautil import stats
    >>> stats.trimean(np.arange(9))
    4.0

    """
    q1 = np.percentile(arr, 25)
    q2 = np.percentile(arr, 50)
    q3 = np.percentile(arr, 75)

    return (q1 + 2 * q2 + q3)/4


def outliers(arr, method='IQR', factor=1.5, percentiles=(5, 95)):
    """ Gets the limits given an array for values to be considered
    outliers.

    :param arr: An array containing numbers.
    :param method: IQR (default) or percentiles.
    :param factor: Factor for the IQR method.
    :param percentiles: A tuple of percentiles.

    :returns: A namedtuple with upper and lower limits.

    >>> import numpy as np
    >>> from dautil import stats
    >>> stats.outliers(a)
    Outlier(min=-48.5, max=149.5)
    """
    Outlier = namedtuple('Outlier', ['min', 'max'])
    outlier = None

    if method == 'IQR':
        q1 = np.percentile(arr, 25)
        q3 = np.percentile(arr, 75)
        iqr = q3 - q1
        outlier = Outlier(q1 - factor * iqr, q3 + factor * iqr)
    elif method == 'percentiles':
        minmax = [np.percentile(arr, p) for p in percentiles]
        outlier = Outlier(minmax[0], minmax[1])
    else:
        raise AssertionError('Unknown method expected IQR or percentiles')

    return outlier


def clip_outliers(arr):
    """ Clips values using limits for values
    to be considered outliers.

    :param arr: An array containing numbers.

    :returns: A clipped values array.

    >>> import numpy as np
    >>> from dautil import stats
    >>> arr = list(range(5))
    >>> outliers = [-100, 100]
    >>> arr.extend(outliers)
    >>> arr
    [0, 1, 2, 3, 4, -100, 100]
    >>> stats.clip_outliers(arr)
    array([ 0.,  1.,  2.,  3.,  4., -4.,  8.])
    """
    amin, amax = outliers(arr)

    return np.clip(arr, amin, amax)


def zscores(x):
    return (x - x.mean())/x.std()


def sqrt_bins(arr):
    """ Uses a rule of thumb to calculate
    the appropriate number of bins for an array.

    :param arr: An array containing numbers.

    :returns: An integer to serve as the number of bins.
    """
    return int(math.sqrt(len(arr)))


def ci(arr, alpha=0.95):
    """ Computes the confidence interval.

    :param arr: An array containing numbers.
    :param alpha: A value in the range 0 - 1\
    that serves as percentiles.

    :returns: The confidence interval.
    """
    interval = 1 - alpha

    minmax = [interval/2, alpha + interval/2]

    return np.percentile(arr, 100 * np.array(minmax))


def jackknife(arr, func, alpha=0.95):
    """ Jackknifes an array with a supplied function.

    :param arr: An array containing numbers.
    :param func: The function to apply.
    :param alpha: A number in the range 0 - 1 used\
    to calculate the confidence interval.

    :returns: Three numbers - the function value for arr,\
    the lower limit of the confidence interval and the\
    upper limit of the confidence interval.
    """
    n = len(arr)
    idx = np.arange(n)

    low, high = ci([func(arr[idx != i]) for i in range(n)], alpha)

    return func(arr), low, high


class Distribution():
    """ Wraps `scipy.stats` distribution classes.
    Most of the methods are only appropriate for continuous distributions.

    :ivar nbins: The number of bins for a histogram plot.
    :ivar train: The train data.
    :ivar test: The test data.
    """
    def __init__(self, data, dist, nbins=20, cutoff=0.75, range=None):
        self.nbins = nbins
        self.train, self.test = self.split(data, cutoff)
        self.hist_values, edges = np.histogram(self.test, bins=self.nbins,
                                               range=range, density=True)
        self.x = 0.5 * (edges[1:] + edges[:-1])
        self.dist = dist
        self.residuals = None
        self.pdf_values = None

    def describe_residuals(self, *args, **kwds):
        """ Describes the residuals of a fit to a distribution.
        Only appropriate for continuous distributions.

        :returns: Statistics for the residuals as a dict.
        """
        _, _, mean, var, skew, kurtosis = describe(self.error(*args, **kwds))
        result = {}
        result['Mean'] = mean
        result['Var'] = var
        result['Skew'] = skew
        result['Kurtosis'] = kurtosis
        result = pd.DataFrame([result])
        result.index = ['Residuals Statistics']

        return result

    def error(self, *args, **kwds):
        """ Computes the residuals of a fit to a distribution.
        Only appropriate for continuous distributions.

        :returns: The residuals of the fit.
        """
        if self.residuals is None:
            self.residuals = self.hist_values - self.pdf(*args, **kwds)

        return self.residuals

    def fit(self, *args):
        """ Fits data to a distribution.
        Only appropriate for continuous distributions.

        :returns: The result of the fit.
        """
        return self.dist.fit(self.train, *args)

    def mean(self):
        return self.train.mean()

    def mean_ad(self, *args, **kwds):
        """ Computes the mean absolute deviation.

        :returns: The mean absolute deviation.
        """
        abserror = np.abs(self.error(*args, **kwds))

        return abserror.mean()

    def pdf(self, *args, **kwds):
        """ Computes the probability distribution function.
        Only appropriate for continuous distributions.

        :returns: The probability distribution function.
        """
        if self.pdf_values is None:
            self.pdf_values = self.dist.pdf(self.x, *args, **kwds)

        return self.pdf_values

    def plot(self, ax):
        """ Plots a histogram of the data and a fit.
        Only appropriate for continuous distributions.
        """
        ax.hist(self.train, bins=self.nbins, normed=True, label='Data')
        ax.plot(self.x, self.pdf_values, label='PDF')
        ax.set_ylabel('Probability')
        ax.legend(loc='best')

    def rmse(self, *args, **kwds):
        """ Computes the root mean square error of the distribution fit.
        Only appropriate for continuous distributions.

        :returns: The RMSE of the fit.
        """
        se = self.error(*args, **kwds) ** 2

        return np.sqrt(se.mean())

    def rvs(self, *args, **kwds):
        """ Generates random values.

        :returns: The generated values.
        """
        return self.dist.rvs(*args, **kwds)

    def split(self, data, cutoff):
        """ Splits data into test and train data.

        :param data: An array containing numbers.
        :param cutoff: A value in the range 0 - 1 used\
        to split the data.

        :returns: Two arrays - the train data and the test data.
        """
        n = len(data)
        n = int(cutoff * n)

        return data[:n], data[n:]

    def var(self):
        return self.train.var()


# TODO Decide on interpolation
class Box():
    ''' Implements the concept of a box we know from box plots. '''
    def __init__(self, arr):
        self.arr = arr
        self.q1 = np.percentile(arr, 25, interpolation='nearest')
        self.q3 = np.percentile(arr, 75, interpolation='nearest')

    def calc_iqr(self):
        """ Calculates the Inter Quartile Range.

        :returns: The interquartile range of the data.

        >>> import numpy as np
        >>> from dautil import stats
        >>> arr = np.array([7, 15, 36, 39, 40, 41])
        >>> box = stats.Box(arr)
        >>> box.calc_iqr()
        25
        """
        return self.q3 - self.q1

    def iqr_from_box(self):
        """ Calculates the number (0 or more) of
        inter quartile ranges (IQR) from the box formed
        by the first and third quartile.

        :returns: A float representing the number of IQRs
        """
        iqr = self.calc_iqr()
        from_q1 = np.abs(self.arr - self.q1)/iqr
        from_q3 = np.abs(self.arr - self.q3)/iqr

        return np.minimum(from_q1, from_q3)
