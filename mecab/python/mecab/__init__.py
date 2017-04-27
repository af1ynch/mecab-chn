from .tfidf import TfIdf
from .MeCab import Tagger
from .textrank import TextRank
from .options import *

default_text_rank = TextRank()
default_tf_idf = TfIdf()
default_tagger = Tagger(WAKATI)

parse = default_tagger.parse
extract_tags = tfidf = default_tf_idf.extract_tags
set_idf_path = default_tf_idf.set_idf_path
text_rank = default_text_rank.extract_tags


def set_stop_words(stop_words_path):
    default_tf_idf.set_stop_words(stop_words_path)
    default_text_rank.set_stop_words(stop_words_path)


