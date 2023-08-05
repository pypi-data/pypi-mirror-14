''' Natural language processing utilities '''
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd


def calc_tfidf(corpus):
    ''' Calculates TF-IDF for a list of text strings and sums it up by term.

    :param corpus: A list of text strings.

    :returns: A pandas `DataFrame` with columns 'term' and 'tfidf'.
    '''
    vectorizer = TfidfVectorizer(ngram_range=(2, 3), stop_words='english')
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
    cutoff = 1000

    if method == 'q3':
        cutoff = np.percentile(df['tfidf'], 75)
    else:
        select_func(df)

    cut_df = df[df['tfidf'] > cutoff]

    return set(cut_df['term'])
