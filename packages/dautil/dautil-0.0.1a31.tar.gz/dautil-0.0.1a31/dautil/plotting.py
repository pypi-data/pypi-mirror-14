""" This module contains plotting utilities. """
from itertools import cycle
from matplotlib.colors import rgb2hex
import matplotlib.pyplot as plt
import numpy as np
from dautil import collect
from dautil import log_api
from dautil import report
from dautil import stats
from matplotlib.markers import MarkerStyle
from scipy.stats import norm


def img_show(ax, img, *args, **kwargs):
    ''' Plots an image with axes turned off.

    :param ax: A `SubplotAxes` object.
    :param img: The image to display.
    '''
    ax.imshow(img, *args, **kwargs)
    ax.axis('off')


def hist_norm_pdf(ax, arr):
    ''' Plots a histogram with corresponding normal PDF.

    :param ax: A `SubplotAxes` object.
    :param arr: Values for the histogram.
    '''
    _, bins, _ = ax.hist(arr, normed=True,
                         bins=stats.sqrt_bins(arr), label='Data')
    ax.plot(bins, norm.pdf(bins, arr.mean(),
                           arr.std()), lw=2, label='Gaussian PDF')
    ax.set_ylabel('Frequency')


def bar(ax, xlabels, vals):
    ''' Plots a bar chart.

    :param ax: A `SubplotAxes` object.
    :param xlabels: Labels on the x-axis.
    :param vals: Values for the bars.
    '''
    xpos = range(len(xlabels))
    ax.bar(xpos, vals, align='center')
    ax.set_xticks(xpos)
    ax.set_xticklabels(xlabels)


def plot_text(ax, xcoords, ycoords, point_labels, add_scatter=False,
              *args, **kwargs):
    ''' Plots text labels with given coordinates.

    :param ax: A `SubplotAxes` object.
    :param xcoords: Array-like x coordinates.
    :param ycoords: Array-like y coordinates.
    :param point_labels: Text labels to put on the chart.
    :param add_scatter: Whether to scatter plot the coordinate values.
    '''
    if add_scatter:
        ax.scatter(xcoords, ycoords)

    for x, y, txt in zip(xcoords, ycoords, point_labels):
        ax.text(x, y, txt, *args, **kwargs)


def all_markers():
    ''' Gets all the matplotlib markers except None.

    :returns: The matplotlib marker character codes except the None markers.
    '''
    return [m for m in MarkerStyle.markers.keys()
            if m is not None or m == 'None']


def map_markers(vals):
    ''' Maps matplotlib markers to values.

    :param vals: Values to map.

    :returns: A list where each value is replaced by a marker character code.
    '''
    uniqs = set(vals)
    markers = cycle(all_markers())
    mark_dict = {u: next(markers) for u in uniqs}

    return [mark_dict[v] for v in vals]


def plot_points(ax, points):
    ''' Plots points with the 'o' marker and as a line.

    :param ax: A `SubplotAxes` object to draw on.
    :param points: A list of points as the following: \
        [(x1, y1), (x2, y2), ...]
    '''
    x, y = zip(*points)
    ax.plot(x, y)
    ax.plot(x, y, 'o')


def plot_polyfit(ax, x, y, degree=1, plot_points=False):
    """ Plots a polynomial fit.

    :param ax: A matplotlib `SubplotAxes` object.
    :param x: An array of 'x' values.
    :param y: An array of 'y' values.
    :param degree: The polynomial degree.
    :param plot_points: Whether to plot points.
    """
    poly = np.polyfit(x, y, degree)

    ax.plot(x, np.polyval(poly, x), label='Fit')

    if plot_points:
        ax.plot(x, y, 'o')


def scatter_with_bar(ax, bar_label, *args, **kwargs):
    """ Creates a matplotlib scatter plot with a colorbar.

    :param ax: A matplotlib `SubplotAxes`.
    :param bar_label: The label of the colorbar.
    """
    sc = ax.scatter(*args, **kwargs)
    plt.colorbar(sc, ax=ax, label=bar_label)


def sample_cmap(name='Reds', start=0.1, end=0.9, ncolors=9):
    """ Samples a matplotlib color map
    using a linearly spaced range.

    :param name: Name of the color map.
    :param start: Start of the linear range.
    :param end: End of the linear range.
    :param ncolors: The number of colors in the range.

    :returns: A sample of the color map.

    >>> from dautil import plotting
    >>> plotting.sample_cmap()
    array([[ 0.99692426,  0.89619378,  0.84890428,  1.        ],
           [ 0.98357555,  0.41279508,  0.28835065,  1.        ],
           [ 0.59461747,  0.0461361 ,  0.07558632,  1.        ]])
    """
    cmap = plt.cm.get_cmap(name)

    return cmap(np.linspace(start, end, ncolors))


def sample_hex_cmap(name='Reds', start=0.1, end=0.9, ncolors=9):
    """ Samples a matplotlib color map
    using a linearly spaced range and
    return hex values for the colors.

    :param name: Name of the color map.
    :param start: Start of the linear range.
    :param end: End of the linear range.
    :param ncolors: The number of colors in the range.

    :returns: A list of hex values from a sample of the color map.

    >>> from dautil import plotting
    >>> plotting.sample_hex_cmap()
    ['#fee5d8', '#fdcab5', '#fcab8f', '#fc8a6a', '#fb694a',
    '#f14432', '#d92523', '#bc141a', '#980c13']
    """
    cmap = sample_cmap(name, start, end, ncolors)

    return [rgb2hex(c) for c in cmap]


def embellish(axes, legends=None):
    """ Adds grid and legends to matplotlib plots.

    :param axes: Axes as returned by the plt.subplots() function.
    :param legends: A list of indices of subplots, which need a legend.
    """
    for i, ax in enumerate(axes):
        ax.grid(True)

        if legends is None:
            ax.legend(loc='best')
        elif i in legends:
            ax.legend(loc='best')


def hide_axes(axes):
    """ Hides the x-axis and y-axis of matplotlib plots.

    :param axes: Axes as returned by the `plt.subplots()` function.
    """
    flat_axes = axes

    if len(axes) > 0:
        flat_axes = axes.ravel()

    for ax in flat_axes:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)


class Cycler():
    """ Utility class, which cycles through values of
    plotting related lists.

    :ivar STYLES: A list of line styles.
    :ivar LW: A list of linewidths.
    :ivar colors: A list of colors.
    """
    def __init__(self, styles=["-", "--", "-.", ":"], lw=[1, 2]):
        self.STYLES = cycle(styles)
        self.LW = cycle(lw)
        self.colors = cycle(sample_hex_cmap(name='hot'))

    def style(self):
        """ Cycles through a list of line styles. """
        return next(self.STYLES)

    def lw(self):
        """ Cycles through a list of linewidth values.

        :returns: The next linewidth in the list.
        """
        return next(self.LW)

    def color(self):
        """ Cycles through a list of colors.

        :returns: The next color in the list.
        """
        return next(self.colors)


class CyclePlotter():
    """ A plotter which cycles through different linestyle
    and linewidth values.

    :ivar ax: A `SubplotAxes` instance.
    :ivar cycler: A `Cycler` instance.
    """
    def __init__(self, ax):
        self.ax = ax
        self.cycler = Cycler()

    def plot(self, x, y=None, *args, **kwargs):
        """ A facade for the matplotlib `plot()` method.

        :param x: Array of 'x' values for the plot.
        :param y: Array of 'y' values for the plot.
        """
        logger = log_api.env_logger()

        if y is None:
            y = x
            x = list(range(len(x)))

        logger.debug('len(x) %s', len(x))
        logger.debug('len(y) %s', len(y))
        self.ax.plot(x, y, self.cycler.style(),
                     lw=self.cycler.lw(), *args, **kwargs)


class Subplotter():
    """ A utility to help with subplotting.

    :ivar context: A `Context` instance.
    :ivar index: The index of the subplot.
    :ivar ax: The current `SubplotAxes` instance.
    """
    def __init__(self, nrows=1, ncols=1, context=None):
        self.context = context
        self.old = None
        self.index = -1

        if context:
            self.old = self.context.read_labels()

            if self.old:
                self.old = collect.flatten(self.old)

        # TODO turn off squeeze
        self.fig, self.axes = plt.subplots(nrows, ncols)

        if nrows > 1 and ncols > 1:
            self.axes = collect.flatten(self.axes)

        if nrows == 1 and ncols == 1:
            self.ax = self.axes
            self.index = 0
        else:
            self.ax_iter = iter(self.axes)
            self.next_ax()

    def next_ax(self):
        """ Advance to next subplot.

        :returns: The current subplot after advancing.
        """
        self.index += 1

        self.ax = next(self.ax_iter)

        return self.ax

    def get_string(self, old, key, params):
        """ Gets a string used to label x-axis,
        y-axis or title of a subplot.

        :param old: Configuration setting from a file.
        :param key: title, xlabel, legend or ylabel.
        :param params: Extra params provided for the
        Python string `format()` method. We expect the
        appropriate use of curly braces.

        :returns: A (formatted) string for the x-axis,
        y-axis, legend or title of a subplot.
        """
        astr = old.get(key, '')

        if params:
            if isinstance(params, str):
                astr = astr.format(params)
            else:
                astr = astr.format(*params)

        return astr

    def label(self, advance=False, title_params=None,
              xlabel_params=None, ylabel_params=None):
        """ Labels the subplot.

        :param advance: Boolean indicating whether to move \
            to the next subplot.
        :param title_params: Optional title parameters.
        :param xlabel_params: Optional xlabel parameters.
        :param ylabel_params: Optional ylabel parameters.
        """
        if advance:
            self.next_ax()

        # Cowardly refusing to continue
        if self.old is None:
            return

        old = self.old[self.index]

        title = self.get_string(old, 'title', title_params)

        if title:
            self.ax.set_title(title)

        xlabel = self.get_string(old, 'xlabel', xlabel_params)

        if xlabel:
            self.ax.set_xlabel(xlabel)

        ylabel = self.get_string(old, 'ylabel', ylabel_params)

        if ylabel:
            self.ax.set_ylabel(ylabel)

        legend = self.get_string(old, 'legend', None)

        if legend.startswith('loc='):
            self.ax.legend(loc=legend.replace('loc=', ''))

    # TODO Decide whether to use a context manager.
    def exit(self, mark=True):
        ''' Cleans up the `Subplotter`.

        :param mark: Boolean indicating whether to apply watermark.

        :returns: The appropriate watermark.
        '''
        plt.tight_layout()
        versions = ''

        if mark:
            versions = report.HTMLBuilder().watermark()

        return versions
