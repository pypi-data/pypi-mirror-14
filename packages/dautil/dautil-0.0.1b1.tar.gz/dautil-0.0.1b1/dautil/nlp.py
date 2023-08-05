''' Natural language processing utilities '''
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from dautil import data
from dautil import log_api
import os
import datetime
from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.corpus import names
from joblib import Memory
from nltk.corpus import words


memory = Memory(cachedir='.')


def has_duplicates(str):
    ''' Checks whether a string has repeating words in it.

    :param str: A string.

    :returns: `True` if the string has repeating words else `False`.
    '''
    tokens = str.split()

    return len(tokens) != len(set(tokens))


def has_digits(str):
    ''' Checks whether a string has digits in it.

    :param str: A string.

    :returns: `True` if the string has digits else `False`.
    '''
    for c in str:
        if c.isdigit():
            return True

    return False


def lower_all(alist):
    ''' Lowercases all words/strings in a list

    :param alist: A list of words/strings.

    :returns: The lowercased words.
    '''
    return [w.lower() for w in alist]


@memory.cache
def common_unigrams():
    ''' Gets the unique words in several corpora in a set.

    :returns: The unique words.
    '''
    sw = set(lower_all(brown.words()))
    sw = sw.union(set(lower_all(names.words())))
    sw = sw.union(set(lower_all(words.words())))
    sw = sw.union(set(lower_all(reuters.words())))

    return sw


def calc_tfidf(corpus, sw='english', ngram_range=(2, 3)):
    ''' Calculates TF-IDF for a list of text strings and sums it up by term.

    :param corpus: A list of text strings.
    :param sw: A list of stop words.

    :returns: A pandas `DataFrame` with columns 'term' and 'tfidf'.
    '''
    if ngram_range:
        vectorizer = TfidfVectorizer(ngram_range=ngram_range, stop_words=sw)
    else:
        vectorizer = TfidfVectorizer(stop_words=sw)

    matrix = vectorizer.fit_transform(corpus)
    sums = np.array(matrix.sum(axis=0)).ravel()

    ranks = [(word, val) for word, val in
             zip(vectorizer.get_feature_names(), sums)]

    df = pd.DataFrame(ranks, columns=["term", "tfidf"])
    df = df.sort(['tfidf'])

    return df


def select_terms(df, method='q3', select_func=None):
    ''' Select terms based on TF-IDF.

    :param df: A pandas `DataFrame` as produced by `calc_tfidf` function.
    :param method: The selection method, \
        default use the third quartile as cutoff.
    :param  select_func: An optional selection function.

    :returns: A set containing the selected terms.
    '''
    cutoff = 0

    if method == 'q3':
        cutoff = np.percentile(df['tfidf'], 75)
    else:
        cutoff = select_func(df['tfidf'])

    cut_df = df[df['tfidf'] > cutoff]

    return set(cut_df['term'])


class WebCorpus():
    ''' A corpus for text downloaded from the Web. '''
    def __init__(self, dir):
        self.dir = os.path.join(data.get_data_dir(), dir)
        self.LOG = log_api.conf_logger(__name__)

        if not os.path.exists(self.dir):
            os.mkdir(self.dir)

        self.csv_fname = os.path.join(self.dir, 'metadata.csv')
        self.url_set = set()
        self.init_url_csv()

    def init_url_csv(self):
        ''' Initialize a CSV containing URLs of downloaded texts. '''

        if os.path.exists(self.csv_fname):
            df = pd.read_csv(self.csv_fname)
            self.url_set = set(df['URL'].values.tolist())
        else:
            with open(self.csv_fname, 'w') as urls_csv:
                urls_csv.write('Added,URL,Title,Author\n')

    def store_text(self, name, txt, url, title, author):
        ''' Stores text in the corpus directory. \
            Also updates a CSV file to avoid downloading the \
            same file again.

        :param name: The name of the file.
        :param txt: The text of the file.
        :param url: The URL of the original document.
        :param title: The title of the original document.
        :param author: The author of the original document.
        '''
        if ',' in url:
            return

        fname = os.path.join(self.dir, name.replace('/', ''))

        try:
            with open(fname, 'w') as txt_file:
                txt_file.write(txt)
        except Exception as e:
            self.LOG.warning(e)

        clean_title = title.replace(',', ' ')
        clean_title = clean_title.replace('/', '')

        with open(self.csv_fname, 'a') as urls_csv:
            timestamp = datetime.datetime.now().isoformat()
            urls_csv.write('{0},{1},{2},{3}\n'.format(
                timestamp, url, clean_title,
                author.replace(',', ' ')))

        self.url_set.add(url)

    def get_texts(self):
        ''' Gets all the texts of the corpus.

        :returns: The texts as a list.
        '''
        texts = []

        for f in os.listdir(self.dir):
            if not f.endswith('.csv') and not f.endswith('.pdf') \
                    and not f.startswith('.'):
                try:
                    with open(os.path.join(self.dir, f), 'r') as txt_file:
                        txt = "".join(txt_file.readlines())

                        if len(txt) > 0:
                            texts.append(txt)
                except Exception as e:
                    self.LOG.warning('{0} {1}'.format(f, e))

        return texts

    def get_text(self, name):
        ''' Gets the text for a file in the corpus.

        :param name: The name of the file.
        :param url: The URL of the original document.

        :returns: The text of the file.
        '''
        txt = ''
        fname = os.path.join(self.dir, name)

        with open(fname, 'r') as txt_file:
            txt = "".join(txt_file.readlines())

        return txt

    def get_titles(self):
        df = pd.read_csv(self.csv_fname)
        return set(self.filter(df['Title'].values.tolist()))

    def get_authors(self):
        df = pd.read_csv(self.csv_fname)
        return set(self.filter(df['Author'].values.tolist()))

    def filter(self, str):
        return [i for i in str if isinstance(i, type('s'))]
