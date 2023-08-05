""" Utilities for time series and dates. """
import pandas as pd
import calendar
import numpy as np
from scipy import signal


def ar1(arr):
    ''' Fits AR(1) model.

    :param arr: array-like, shape(M,)

    :returns A dictionary with slope and intercept of the model.
    '''
    slope, intercept = np.polyfit(arr[:-1], arr[1:], 1)

    return {'slope': slope, 'intercept': intercept}


def power(arr):
    ''' Computes the power of a signal.

    :param arr: Array-like list of values.

    :returns: The power of a signal.
    '''
    return np.abs(arr) ** 2


def instant_phase(arr):
    ''' Computes the instaneous phase of a signal.

    :param arr: Array-like list of values.

    :returns: The instaneous phase.
    '''
    return np.angle(signal.hilbert(arr))


def double_exp_smoothing(arr, alpha, beta):
    ''' Applies double exponential smoothing.

    .. math::
        \\begin{align}
        s_{t} = \\alpha x_{t} + (1-\\alpha)(s_{t-1} + b_{t-1})\\\\
        b_{t} = \\beta (s_t - s_{t-1}) + (1-\\beta)b_{t-1}\\\\
        \\end{align}

    :param arr: Array-like list of values.
    :param alpha: The smoothing factor parameter.
    :param beta: The trend factor parameter.

    :returns: The smoothed series values.
    '''
    st = arr.copy()
    bt = arr.copy()
    bt[0] = (arr[-1] - arr[0])/len(arr)
    bt[1] = arr[1] - arr[0]

    for i, val in enumerate(arr[1:], start=1):
        st[i] = alpha * val + (1 - alpha) * (st[i - 1] + bt[i - 1])
        bt[i] = beta * (st[i] - st[i - 1]) + (1 - beta) * bt[i - 1]

    return st


def exp_smoothing(arr, alpha):
    ''' Applies exponential smoothing.

    .. math:: s_t = \\alpha \\cdot x_{t} + (1-\\alpha) \\cdot s_{t-1}

    :param arr: Array-like list of values.
    :param alpha: The smoothing factor parameter.

    :returns: The smoothed series values.
    '''
    st = arr.copy()

    for i, val in enumerate(arr[1:], start=1):
        st[i] = alpha * val + (1 - alpha) * st[i - 1]

    return st


def rolling_deviations(arr, window):
    ''' Computes the rolling deviations of a series, by subtracting \
        the rolling mean and dividing by the rolling standard deviation.

    :param arr: Array-like list of values.
    :param window: Size of the window.

    :returns: The rolling deviations.
    '''
    return (arr - pd.rolling_mean(arr, window))/pd.rolling_std(arr, window)


def fano_factor(arr, window):
    ''' Calculates the Fano factor a windowed variance-to-mean ratio.

    .. math:: F=\\frac{\\sigma_W^2}{\\mu_W}

    :param arr: Array-like list of values.
    :param window: Size of the window.

    :returns: The Fano factor.

    *See Also*

    https://en.wikipedia.org/wiki/Fano_factor
    '''
    return pd.rolling_var(arr, window)/pd.rolling_mean(arr, window)


def sine_like(arr):
    ''' Creates a sine wave of roughly the same size as the input.

    :param arr: Array-like list of values.

    :returns: A sine wave.
    '''
    t = np.linspace(-2 * np.pi, 2 * np.pi, len(arr))
    mid = np.ptp(arr)/2

    return mid + mid * np.sin(t)


def groupby_yday(df):
    """ Groups a pandas DataFrame by the day of year.

    :param df: A pandas `DataFrame`.

    :returns: The grouped `DataFrame`.
    """
    return df.groupby(lambda d: d.timetuple().tm_yday)


def groupby_month(df):
    """ Groups a pandas `DataFrame` by month.

    :param df: A pandas `DataFrame`.

    :returns: The grouped `DataFrame`.
    """
    return df.groupby(df.index.month)


def groupby_year(df):
    """ Groups a pandas `DataFrame` by year.

    :param df: A pandas `DataFrame`.

    :returns: The grouped `DataFrame`.
    """
    return df.groupby(df.index.year)


def groupby_year_month(df):
    """ Groups a pandas `DataFrame` by year and month.

    :param df: A pandas `DataFrame`.

    :returns: The grouped `DataFrame`.
    """
    return pd.groupby(df, by=[df.index.year, df.index.month])


def short_month(i, zero_based=False):
    """ Looks up the short name of a month with an index.

    :param i: Index of the month to lookup.
    :param zero_based: Indicates whether the index starts from 0.

    :returns: The short name of the month for example Jan.

    >>> from dautil import ts
    >>> ts.short_month(1)
    'Jan'
    """
    j = i

    if zero_based:
        if i < 0 or i > 11:
            raise AssertionError("Out of range " + i)

        j = i + 1

    return calendar.month_abbr[j]


def short_months():
    """ Gets the short names of the months.

    :returns: A list containing the short month names.
    """
    return [short_month(i) for i in range(13)]


def month_index(month, zero_based=False):
    """ Looks up the index of a month from a short name.

    :param month: The short name of a month to lookup for example Jan.
    :param zero_based: Indicates whether the index starts from 0.

    :returns: The index of the month.

    >>> from dautil import ts
    >>> ts.month_index('Jan')
    1
    """
    for i, m in enumerate(short_months()):
        if m == month:
            index = i

            if not zero_based:
                index += 1

            return i
