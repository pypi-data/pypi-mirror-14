''' Utilities for web mining and HTML processing. '''
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse as urlparse
import urllib.request as urlrequest


def path2url(path):
    ''' Transforms file paths to URLs starting with file:

    :param path: The file path.

    :returns: The corresponding URL.

    >>> from dautil import web
    >>> web.path2url('/home/dautil')
    'file:///home/dautil'
    '''
    return urlparse.urljoin('file:', urlrequest.pathname2url(path))


def find_hrefs(content):
    ''' Finds href links in a HTML string.

    :param content: A HTML string.

    :returns: A list of href links found by BeautifulSoup.
    '''
    soup = BeautifulSoup(content)

    return [a.get('href', '') for a in soup.findAll('a')]


def wait_browser(browser, selector, secs=10, by=By.XPATH):
    ''' Waits for a HTML element to become available.

    :param browser: An instance of a Selenium browser.
    :param selector: An expression used to select the web element.
    :param by: The selection method such as XPath or tag name.

    :returns: The web element you are waiting for.
    '''
    return WebDriverWait(browser, secs).until(
        EC.presence_of_element_located((by, selector))
    )
