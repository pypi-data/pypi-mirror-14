# Temporary I think
import warnings
warnings.filterwarnings(action='ignore',
                        message='.*IPython widgets are experimental.*')
import logging

logging.basicConfig()
LOGGER = logging.getLogger(__name__)

from .nb import *
from .options import *
from .plotting import *

try:
    from .report import *
except ImportError as e:
    LOGGER.warning('Could not import report module %s', e)

from .stats import *

try:
    from .web import *
except ImportError as e:
    LOGGER.warning('Could not import web module %s', e)

try:
    from .db import *
except ImportError as e:
    LOGGER.warning('Could not import db module %s', e)

try:
    from .perf import *
except ImportError as e:
    LOGGER.warning('Could not import perf module %s', e)

try:
    from .nlp import *
except ImportError as e:
    LOGGER.warning('Could not import nlp module %s', e)
