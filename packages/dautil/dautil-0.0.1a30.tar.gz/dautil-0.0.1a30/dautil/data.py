""" Utilities to download and load data. """
import pandas as pd
from pandas.io import wb
from pandas.io.data import DataReader
import numpy as np
from io import BytesIO
import zipfile
import gzip
from appdirs import AppDirs
import os
from pkg_resources import resource_filename
import urllib.request as urlrequest
from dautil import log_api
from dautil import options
from collections import namedtuple
from joblib import Memory
import csv
from decimal import Decimal
from datetime import datetime
import pickle


def from_pickle(fname):
    ''' Loads object from pickle.

    :param fname: The name of the pickle file.

    :returns: The object from the pickle.
    '''
    pkl = open(fname, 'rb')
    obj = pickle.load(pkl)
    pkl.close()

    return obj


def centify(text, multiplier=100):
    ''' Converts a string representing money\
        to the corresponding number in cents.

    :param text: A string such as 10.55.
    :param multiplier: A multiplier for the conversion.
    :returns: Cents as an integer, for instance 1055.

    >>> from dautil import data
    >>> data.centify('10.55')
    1055
    '''
    return int(multiplier * Decimal(text))


def dropinf(arr):
    """ Removes `np.inf` and `np.nan` values.

    :param arr: Array with numbers.

    :returns: The cleaned array.

    >>> from dautil import data
    >>> import numpy as np
    >>> arr = np.array([np.inf, 0, 42, np.nan])
    >>> data.dropinf(arr)
    array([  0.,  42.])
    """
    return arr[np.isfinite(arr)]


def download(url, out):
    """ Download a file from the web.

    :param url: The URL of the file.
    :param out: The path of the file.
    """
    req = urlrequest.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlrequest.urlopen(req)

    with open(out, 'wb') as data_file:
        data_file.write(res.read())
        log_api.conf_logger(__name__).warning('Downloaded ' + data_file.name)


def process_gzip(url, file_path):
    """ Downloads and uncompresses a GZIP file.

    :param url: The URL of the GZIP file.
    :param file_path: The path of the file.
    """
    response = urlrequest.urlopen(url)
    compressed = BytesIO(response.read())
    decompressed = gzip.GzipFile(fileobj=compressed)

    with open(file_path, 'wb') as outfile:
        outfile.write(decompressed.read())


def process_zip(url, path, fname):
    """ Downloads and uncompresses a ZIP file.

    :param url: The URL of the ZIP file.
    :param path: The path of the file.
    :param fname: The name of the file.

    :returns: The contents of the extracted file.
    """
    response = urlrequest.urlopen(url)

    zipf = zipfile.ZipFile(BytesIO(response.read()))

    return zipf.extract(fname, path)


def get_data_dir():
    """ Finds the appropriate data directory to store data files.

    :returns: A data directory, which is OS dependent.
    """
    dirs = AppDirs(options.APP_DIR, "Ivan Idris")
    path = dirs.user_data_dir
    log_api.conf_logger(__name__).warning('Data dir ' + path)

    if not os.path.exists(path):
        os.mkdir(path)

    return path


def get_direct_marketing_csv():
    ''' Retrieves a CSV file with direct marketing data as described in \
        http://blog.minethatdata.com/2008/03/ \
        minethatdata-e-mail-analytics-and-data.html

    :returns: The path to the downloaded file.
    '''
    base_url = 'https://azuremlsampleexperiments.blob.core.windows.net/'
    url = base_url + 'datasets/direct_marketing.csv'
    out = os.path.join(get_data_dir(), 'direct_marketing.csv')

    if not os.path.exists(out):
        download(url, out)

    return out


def get_smashing_baby():
    ''' Retrieves a WAV file of Austin Powers.

    :returns: The path to the downloaded file.
    '''
    base_url = 'http://www.thesoundarchive.com/'
    url = base_url + 'austinpowers/smashingbaby.wav'
    out = os.path.join(get_data_dir(), 'smashingbaby.wav')

    if not os.path.exists(out):
        download(url, out)

    return out


def read_csv(fname):
    ''' Reads a CSV file and returns a list of dictionaries \
        where each line corresponds to a line in the file.

    :param fname: The name or path of the file.

    :returns: The dictionary.
    '''
    csv_rows = []

    with open(fname) as afile:
        reader = csv.DictReader(afile)

        csv_rows = [row for row in reader]

    return csv_rows


class Nordpil():
    """ Utility class to get data from the Nordpil website.

    :ivar dir: The data destination directory.
    """
    def __init__(self):
        self.dir = get_data_dir()

    def load_urban_tsv(self):
        """ Downloads the urbanareas file.

        :returns: The fully qualified path of the downloaded file.
        """
        fname = os.path.join(self.dir,
                             'urbanareas1_1.tsv')

        if not os.path.exists(fname):
            download('http://nordpil.com/static/downloads/urbanareas1_1.tsv',
                     fname)

        return fname


class SPANFB():
    """ Utility class which downloads data from the
    SPAN Facebook webpage.
    :ivar fname: The path of the downloaded file.
    """
    def __init__(self):
        self.fname = os.path.join(get_data_dir(),
                                  'facebook_combined.txt')

    def load(self):
        """ Downloads the SPAN Facebook dataset.

        :returns: The fully qualified path of the downloaded file.
        """
        if not os.path.exists(self.fname):
            process_gzip(
                'https://snap.stanford.edu/data/facebook_combined.txt.gz',
                self.fname)

        return self.fname


class Weather():
    """ Utility class which downloads or loads weather data
    from the KNMI website. """
    @staticmethod
    def beaufort_scale(df):
        """ Categorizes wind speed using the Beaufort scale.
        :param df: A pandas `DataFrame`.

        :returns: A categorized pandas `DataFrame`.
        """
        return pd.cut(df['WIND_SPEED'], bins=[0, 0.3, 1.5, 3.3, 5.5, 8, 10.8,
                                              13.9, 17.2, 20.7, 24.5, 28.4,
                                              32.6, np.inf],
                      labels=np.arange(13, dtype=np.int))

    @staticmethod
    def categorize_wind_dir(df):
        """ Categorize the wind direction (0 - 360) using
        cardinal direction (North, South etc.)

        :param df: A pandas `DataFrame`.

        :returns: A categorized pandas `DataFrame`.
        """
        card_dirs = ['Calm', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
        deg_rngs = [0, 11.25, 33.75, 56.25, 78.75, 101.25, 123.75, 146.25,
                    168.75, 191.25, 213.75, 236.25, 258.75, 281.25, 303.75,
                    326.25, 348.75, 360]

        return pd.cut(df['WIND_DIR'], deg_rngs, labels=card_dirs)

    @staticmethod
    def load():
        """ Loads data from an internal pickle.

        :returns: The pandas `DataFrame` loaded from the pickle.
        """
        pckl = resource_filename(__name__, 'weather.pckl')
        return pd.read_pickle(pckl)

    @staticmethod
    def rain_values():
        """ Loads rain values without NA values as a NumPy array.

        :returns: The rain values as a NumPy array.
        """
        return Weather.load()['RAIN'].dropna().values

    @staticmethod
    def get_header(alias):
        """ Gets slightly longer and descriptive column labels.

        :param alias: A short column name.

        :returns: A longer column name.
        """
        mapping = {'WIND_DIR': 'Wind Dir',
                   'WIND_SPEED': 'W Speed, m/s',
                   'TEMP': 'Temp, °C',
                   'RAIN': 'Rain, mm',
                   'PRESSURE': 'Pres, hPa'}

        return mapping.get(alias, 'UNKNOWN')

    @staticmethod
    def get_headers():
        """ Gets the column labels for the pandas `DataFrame`
        stored in the internal pickle.

        :returns: A list that contains the column names.
        """
        return ['WIND_DIR', 'WIND_SPEED', 'TEMP', 'RAIN', 'PRESSURE']

    @staticmethod
    def fetch_DeBilt_weather():
        """ Downloads, cleans and pickles weather data from the
        KNMI website. """
        home = 'http://www.knmi.nl/'
        url = home + 'klimatologie/daggegevens/datafiles3/260/etmgeg_260.zip'
        path = get_data_dir()
        file = process_zip(url, path, 'etmgeg_260.txt')
        df = pd.read_csv(
            file,
            skiprows=47,
            usecols=[
                'YYYYMMDD',
                'DDVEC',
                '   FG',
                '   TG',
                '   RH',
                '   PG'],
            index_col=0,
            parse_dates=True,
            na_values='     ')

        df.columns = ['WIND_DIR', 'WIND_SPEED', 'TEMP', 'RAIN', 'PRESSURE']
        df[df['RAIN'] == -1] = 0.05 / 2
        df['WIND_SPEED'] = 0.1 * df['WIND_SPEED']
        df['TEMP'] = 0.1 * df['TEMP']
        df['RAIN'] = 0.1 * df['RAIN']
        df[df['PRESSURE'] < 1] = np.nan
        df['PRESSURE'] = 0.1 * df['PRESSURE']
        log_api.conf_logger(__name__).warning(df.index[-1])

        pckl = os.path.join(path, 'weather.pckl')
        df.to_pickle(pckl)
        assert df.equals(pd.read_pickle(pckl))


class OHLC():
    ''' Downloads and caches historical EOD data from the web.
        with the `pandas.io.data.DataReader`.
    '''
    def __init__(self, data_source='yahoo'):
        ''' Creates the object and sets up caching.

        :param data_source: A data souce such as `yahoo` or `google`.
        '''
        self.data_source = data_source
        # caching
        memory = Memory(cachedir='.')
        self.get = memory.cache(self.get)

    def get(self, ticker):
        ''' Retrieves EOD data from cache or the web.

        :param ticker: The stock symbol, such as `AAPL`.

        :returns: The data as a pandas `DataFrame`.
        '''
        start = datetime(1900, 1, 1, 0, 0, 0, 0)
        return DataReader(ticker, data_source=self.data_source, start=start)


class Worldbank():
    """ Caching proxy for the pandas Worldbank API.

    :ivar indicators: A list of indicator tuples in the form: \
        `(alias, name, longname)`
    :ivar alias2name: Mapping of alias to name.
    :ivar name2alias: Mapping of name to alias.
    :ivar name2longname: Mapping of name to longname.
    :ivar aliases: A list of aliases.
    :ivar names: A list of indicator names.
    """
    def __init__(self):
        # TODO make this configurable
        Indicator = namedtuple('Indicator', ['alias', 'name', 'longname'])
        self.indicators = [Indicator(alias='pop_grow', name='sp.pop.grow',
                                     longname='Population Growth'),
                           Indicator(alias='gdp_pcap', name='ny.gdp.pcap.cd',
                                     longname='GDP Per Capita'),
                           Indicator(alias='co2', name='en.atm.co2e.kt',
                                     longname='CO2 emissions (kt)'),
                           Indicator(alias='inf_mort', name='sh.dyn.mort',
                                     longname='Mortality rate, \
                                     under-5 (per 1,000 live births)'),
                           Indicator(alias='primary_education',
                                     name='se.prm.cmpt.zs', longname='Primary\
                                     Education Completion Rate')]
        self.alias2name = {i.alias: i.name for i in self.indicators}
        self.name2alias = {j: i for i, j in self.alias2name.items()}
        self.name2longname = {i.name: i.longname for i in self.indicators}
        self.aliases = self.alias2name.keys()
        self.names = self.alias2name.values()

        # caching
        memory = Memory(cachedir='.')
        self.download = memory.cache(self.download)
        self.get_countries = memory.cache(self.get_countries)

    def get_countries(self, *args, **kwargs):
        """ Caches the `pandas.io.wb.get_countries()` results.

        :returns: The result of the query from cache or the WWW.
        """
        return wb.get_countries(*args, **kwargs)

    def download(self, *args, **kwargs):
        """ Caches the `pandas.io.wb.download()` results.

        :returns: The result of the query from cache or the WWW.
        """
        return wb.download(*args, **kwargs)

    def get_alias(self, name):
        """ Gets an internal alias for the official
        Worldbank indicator.

        :param name: The name of the Worldbank indicator.

        :returns: The internal alias.
        """
        assert name in self.names, self.indicators

        return self.name2alias[name]

    def get_name(self, alias):
        """ Gets the official Worldbank indicator
        for an internal alias.

        :param alias: The internal alias.

        :returns: The name of the Worldbank indicator.
        """
        assert alias in self.aliases, self.indicators

        return self.alias2name[alias]

    def get_longname(self, name):
        """ Gets a longer descriptive name for a
        Worldbank indicator.

        :param name: The name of a Worldbank indicator.

        :returns: The long descriptive name.
        """
        assert name in self.names, self.indicators

        return self.name2longname[name]

    def rename_columns(self, df, use_longnames=False):
        """ Renames the columns of a pandas `DataFrame`.

        :param df: A pandas `DataFrame`.
        :param use_longnames: Whether to use longnames for the renaming.

        :returns: The pandas DataFrame with its columns renamed.
        """
        new_cols = []

        for col in df.columns:
            if use_longnames:
                if col in self.names:
                    new_cols.append(self.name2longname[col])
                else:
                    new_cols.append(col)
            else:
                if col in self.names:
                    new_cols.append(self.name2alias[col])
                else:
                    new_cols.append(col)

        df.columns = new_cols

        return df
