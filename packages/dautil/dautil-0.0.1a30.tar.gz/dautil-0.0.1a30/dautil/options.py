""" Configures dynamic options of several
data analysis related libraries. """
import pandas as pd
import matplotlib as mpl
import numpy as np


APP_DIR = 'dautil'


def mimic_seaborn():
    """ Mimics the Seaborn style with small deviations. """
    sns_style = {'axes.axisbelow': True,
                 'axes.edgecolor': 'white',
                 'axes.facecolor': '#EAEAF2',
                 'axes.grid': True,
                 'axes.labelcolor': '.15',
                 'axes.linewidth': 0,
                 'font.family': 'Arial',
                 # deviating
                 'grid.color': 'yellow',
                 'grid.linestyle': '-',
                 # deviating
                 'grid.linewidth': 2,
                 'image.cmap': 'Greys',
                 'legend.frameon': False,
                 'legend.numpoints': 1,
                 'legend.scatterpoints': 1,
                 'lines.solid_capstyle': 'round',
                 'pdf.fonttype': 42,
                 'text.color': '.15',
                 'xtick.color': '.15',
                 'xtick.direction': 'out',
                 'xtick.major.size': 0,
                 'xtick.minor.size': 0,
                 'ytick.color': '.15',
                 'ytick.direction': 'out',
                 'ytick.major.size': 0,
                 'ytick.minor.size': 0}
    mpl.rcParams.update(sns_style)


def set_pd_options():
    """ Sets pandas options. """
    pd.set_option('precision', 4)
    pd.set_option('max_rows', 5)


def reset_pd_options():
    """ Resets pandas options. """
    pd.reset_option('precision')
    pd.reset_option('max_rows')


def set_mpl_options():
    """ Sets matplotlib options. """
    mpl.rcParams['legend.fancybox'] = True
    mpl.rcParams['legend.shadow'] = True
    mpl.rcParams['legend.framealpha'] = 0.7


def set_np_options():
    """ Sets NumPy options. """
    np.set_printoptions(precision=4, threshold=5,
                        linewidth=65)


def reset_np_options():
    """ Resets NumPy options. """
    np.set_printoptions(precision=8, threshold=1000,
                        linewidth=75)
