""" This module contains reporting utilities. """
import pandas as pd
from landslide.generator import Generator as LandslideGenerator
from dautil import data
from dautil import log_api
import os
import sys


def map_grid(a, b, cols, func, *args, **kwargs):
    ''' Apply a function to the cells of a grid.

    :param a: One of two arrays used to form the grid.
    :param b: One of two arrays used to form the grid.
    :param cols: A list of column names.
    :param func: Function to apply.

    :returns: A pandas `DataFrame` containing the result.
    '''
    dfb = DFBuilder(cols=cols)

    for i in a:
        for j in b:
            dfb.row([i, j, func(i, j, *args, **kwargs)])

    return dfb.build().pivot(*cols)


class DFBuilder():
    """ Builds a pandas `DataFrame`,
    by updating a dict incrementally.

    The actual `DataFrame` is built at the end
    of the build process.

    :ivar columns: The columns of the `DataFrame`.
    :ivar df: The `DataFrame`.
    """
    def __init__(self, cols, *args):
        self.columns = cols
        self.df = {}

        for col in self.columns:
            self.df.update({col: []})

        for arg in args:
            self.row(arg)

    def row(self, row):
        """ Adds a row to the pandas DataFrame

        :param row: A list of values to add.

        :returns: A table-like dict.

        >>> from dautil import report
        >>> builder = report.DFBuilder(['A', 'B'])
        >>> row = list(range(2))
        >>> builder.row(row)
        {'B': [1], 'A': [0]}
        >>> builder.df
        {'B': [1], 'A': [0]}
        """
        assert len(row) == len(self.columns),\
            '{0} != expected len {1}'.format(len(row), len(self.columns))

        for col, val in zip(self.columns, row):
            self.df[col].append(val)

        return self.df

    def build(self, index=None):
        """ Builds a pandas `DataFrame` from an internal dict.

        :param index: A list representing the `DataFrame` index.

        :returns: A pandas `DataFrame`.
        """
        self.df = pd.DataFrame(self.df)

        if index:
            self.df.index = index

        return self.df


class RSTWriter():
    """ Writes a reStructured text file.

    :ivar rst: A string representing reStructured text.
    """
    def __init__(self):
        self.rst = ''

    def h1(self, txt):
        """ Adds a first level heading.

        :param txt: The text of the heading.
        """
        self.rst += txt + '\n'
        self.rst += ('=' * len(txt)) + '\n\n'

    def add(self, txt):
        """ Adds arbitrary text.

        :param txt: The text to add.
        """
        self.rst += txt

    def divider(self):
        """ Adds a divider. """
        self.rst += '\n\n----\n\n'

    def write(self, fname):
        """ Writes to a file.

        :param fname: The name of the file.
        """
        with open(fname, 'w') as f:
            f.write(self.rst)
            log_api.conf_logger(__name__).warning('Wrote to ' + fname)


# TODO read styles from file
# TODO add css params
class HTMLBuilder():
    """ Builds a HTML string.

    :ivar html: A string representing HTML.
    """
    def __init__(self):
        self.html = ''

    def h1(self, heading):
        """ Adds a first level heading.

        :param heading: The text of the heading.
        """
        style = "border-top: dashed 1px gray;"
        tag = '<h1 style="{0}">{1}</h1>'
        self.html += tag.format(style, heading)
        self.watermark()

    def h2(self, heading):
        """ Adds a second level heading.

        :param heading: The text of the heading.

        >>> from dautil import report
        >>> hb = report.HTMLBuilder()
        >>> hb.h2('Heading 2')
        >>> hb.html
        '<h2 style="color:gray;">Heading 2</h2><br/>'
        """
        style = 'color:gray;'
        self.html += '<h2 style="{0}">{1}</h2><br/>'.format(style, heading)

    def add(self, text):
        """ Adds arbitrary html.

        :param txt: The html to add.


        >>> from dautil import report
        >>> hb = report.HTMLBuilder()
        >>> hb.add('<p>42</p>')
        >>> hb.html
        '<div><p>42</p></div><br/>'
        """
        self.html += '<div>{}</div><br/>'.format(text)

    def add_df(self, df, index=False, *args, **kwargs):
        """ Converts a pandas `DataFrame` to HTML and adds it.

        :param df: A pandas `DataFrame`.
        :param index: Boolean indicating whether to display the index.
        """
        # TODO handle css properly
        classes = """
            tr:nth-child(odd)		{ background-color:#eee; }
            tr:nth-child(even)		{ background-color:#fff; }
            """

        self.html += '<div>{}</div><br/>'.format(
            df.to_html(index=index, classes=classes, *args, **kwargs))

    def __add__(self, other):
        if isinstance(other, pd.DataFrame):
            self.add_df(other)
        else:
            self.add(other)

        return self

    def watermark(self):
        """ Adds a watermark containing versions of
        detected software libraries.

        :returns: The HTML of the watermark.
        """
        versions = log_api.log(sys.modules, 'HTMLBuilder')
        style = "font-size:5px;"
        vlist = []

        for k, v in versions.items():
            vlist.append('{0}={1}'.format(k, v))

        tag = '<p style="{0}">Tested with {1}</p>'
        self.html += tag.format(style, ', '.join(vlist))

        return self.html


class Generator():
    CSS = "https://www.googledrive.com/host/0B8Dd5LtC555uNTJQXzZKdDN4aWc"

    def __init__(self, rst_file, out):
        self.dir = data.get_data_dir()
        self.out_file = os.path.join(self.dir, out)
        self.gen = LandslideGenerator(rst_file, destination_file=self.out_file)

    def add_css(self):
        css = os.path.join(self.dir, 'report.css')
        data.download(self.CSS, css)
        self.gen.add_user_css([css])

    def generate(self):
        self.add_css()
        self.gen.write()

        log_api.conf_logger(__name__).warning('Generated HTML in ' +
                                              self.out_file)
