""" Logging utilities. """
from pkg_resources import get_distribution
from pkg_resources import resource_filename
from pkg_resources import DistributionNotFound
import logging
import logging.config
import pprint
from appdirs import AppDirs
import os
from dautil import conf
from dautil import options
import inspect


def env_logger():
    """ Creates a configurable logger.
    The environment variable **DAUTIL_LOGGER** controls
    whether the logger is enabled.
    If the value of the variable is *, then all loggers
    will be enabled, otherwise the calling function name
    is matched against `DAUTIL_LOGGER`.
    Enabling/disabling the logger may be influenced by
    an underlying framework.

    :returns: A configurable logger.
    """
    frame = inspect.stack()[1]
    func_name = frame[3]
    env_val = os.environ.get('DAUTIL_LOGGER')
    log_enabled = False

    if env_val:
        if env_val == '*':
            log_enabled = True
        elif func_name in env_val:
            log_enabled = True

    logger = conf_logger(func_name)

    if not log_enabled:
        logger.addHandler(logging.NullHandler())
        # Needed for ipython notebook sessions
        logger.propagate = False

    return logger


def get_logger(name):
    """ Creates a logger using an internal configuration file.

    :param name: The name of the logger.

    :returns: The configured logger.
    """
    log_config = resource_filename(__name__, 'log.conf')
    logging.config.fileConfig(log_config)
    logger = logging.getLogger(name)

    return logger


def conf_logger(name):
    """ Creates a logger using a configuration file
    provided by the user in the current working directory.
    If a configuration file is not found, dautil uses
    basic configuration.

    :param name: The name of the logger.

    :returns: The configured logger.
    """
    # TODO check for conf file in appropriate dir
    conf_file = 'dautil_log.conf'

    if conf.file_exists(conf_file):
        logging.config.fileConfig(conf_file, disable_existing_loggers=False)
    else:
        logging.basicConfig()

    return logging.getLogger(name)


def shorten(module_name):
    """ Helper function which shortens a module name
    using the first occurrence of a dot. For example
    pandas.io.wb is shortened to pandas.

    :param module_name: The name of the module.

    :returns: The shortened name.

    >>> from dautil import log_api
    >>> log_api.shorten('pandas.io.wb')
    'pandas'
    """
    dot_i = module_name.find('.')

    return module_name[:dot_i]


def log(modules, name):
    """ Logs the versions of imported modules in a
    best effort fashion. Some common modules are excluded.

    :param modules: A list of modules as available in sys.modules.
    :param name: The name of the logger.

    :returns: A dictionary with modules as keys and versions as values.
    """
    skiplist = ['pkg_resources', 'distutils', 'zmq']

    logger = get_logger(name)
    logger.debug('Inside the log function')
    versions = {}

    for k in modules.keys():
        str_k = str(k)

        if '.version' in str_k:
            short = shorten(str_k)

            if short in skiplist:
                continue

            try:
                ver = get_distribution(short).version
                logger.info('%s=%s' % (short, ver))
                versions[short] = ver
            except ImportError:
                logger.warn('Could not import', short)
            except DistributionNotFound as e:
                logger.warn('Could not find distribution %s', e)

    return versions


class VersionsLogFileHandler(logging.FileHandler):
    """ A specialized file handler for the logging of software versions. """
    def __init__(self, fName):
        dirs = AppDirs(options.APP_DIR, "Ivan Idris")
        path = dirs.user_log_dir
        print(path)

        if not os.path.exists(path):
            os.mkdir(path)

        super(VersionsLogFileHandler, self).__init__(
              os.path.join(path, fName))


class Printer():
    """ Utility class for pretty printing.

    :ivar nelems: Max number of elements in a list to print.
    """
    def __init__(self, modules=None, name=None, nelems=-1):
        if modules and name:
            log(modules, name)

        self.nelems = nelems

    def print(self, *args, **kwargs):
        """ Pretty prints a message. """
        for arg in args:
            if self.nelems > 0 and isinstance(arg, list):
                pprint.pprint(self.compress_mid(arg), **kwargs)
            else:
                pprint.pprint(arg, **kwargs)

        print()

    def compress_mid(self, alist, replace='...'):
        """ Takes the head, mid and the tail of a list \
            and discards the rest. For example

        >>> from dautil import log_api
        >>> p = log_api.Printer(nelems=3)
        >>> p.compress_mid(list(range(5)))
        [0, '...', 2, '...', 4]

        :param alist: A list.
        :param replace: A string used to replace discarded elements.

        :returns: The list with discarded values replaced.
        """
        compressed = alist.copy()
        N = len(alist)

        if N > self.nelems:
            half = self.nelems//2
            mid = N//2
            logger = env_logger()
            compressed = alist[:half]

            for i in range(half, N - half):
                if i != mid and compressed[-1] != replace:
                    compressed.append(replace)
                    logger.debug('Compressed %s', compressed)
                if i == mid:
                    compressed.append(alist[mid])

            compressed.extend(alist[-half:])

        return compressed
