"""
Tweet proccessor
this contains a python class called TweetProcessor
This class process a given tweet in as requested.
currently available actions are:
    - Tokenization
    - Removing noise data(hyperlinks and etc.)
    - Removing specific characters or tokens
    - Part of speech tagging
    - Stemming
    - Lematizing
    - N-gram Generator

these tasks are done with nltk package. An opensource python package for processing the natural language
"""
__author__ = "Matin Ebrahimkhani"
__copyright__ = "Copyright 2020, twitter analysis for covid tweets with nltk project"
__credits__ = ["Matin Ebrahimkhani"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Matin Ebrahimkhani"
__email__ = "mat.ebrahimkhani@iasbs.ac.ir"
__studentID__: str = "994121"

import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
from nltk.util import ngrams


class TweetProcessor:
    def __init__(self):
        self.lematizer_method = WordNetLemmatizer()
        self.stemmer_method = PorterStemmer()

    def tokenize(self, tweet: str):
        result = word_tokenize(tweet)
        return result  # : [hi , ]

    def remove_noise(self, tweet: list):
        result = []
        for token in tweet:
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|'
                           '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)  # removing hyperlinks
            token = re.sub("(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)", "", token)  # removing hashtags and mentions
            token = re.sub("([0-9]+)", "", token)  # removing numbers
            if token not in ['', " ", ' ']:
                result.append(token)
        return result

    def remove(self, tweet: list, removable):
        result = []
        if type(removable) is list or str:
            for token in tweet:
                if token.lower() not in removable:
                    result.append(token)
        return result

    def tag_pos(self, tweet: list):

        return pos_tag(tweet)

    def stem(self, tweet: list):
        result = []
        for word in tweet:
            result.append(self.stemmer_method.stem(word))

        return result

    def lematize(self, tweet: list):
        result = []
        for word, tag in tweet:
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            result.append((self.lematizer_method.lemmatize(word, pos), tag))
        return result

    def extract_ngrams(self, tweet: list, num):
        return ngrams(tweet, num)
