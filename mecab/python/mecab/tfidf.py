#! /usr/bin/env python

# encoding=utf-8

import sys
from .MeCab import Tagger
import os
from operator import itemgetter
from .pair import Pair

_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__), path))
_get_abs_path = lambda path: os.path.normpath(os.path.join(os.getcwd(), path))

DEFAULT_PATH = _get_module_path("idf.txt")


class KeywordExtractor(object):

    STOP_WORDS = set((
        "the", "of", "is", "and", "to", "in", "that", "we", "for", "an", "are",
        "by", "be", "as", "on", "with", "can", "if", "from", "which", "you", "it",
        "this", "then", "at", "have", "all", "not", "one", "has", "or", "that"
    ))

    def set_stop_words(self, stop_words_path):
        abs_path = _get_abs_path(stop_words_path)
        if not os.path.isfile(abs_path):
            raise Exception("file does not exist: " + abs_path)
        content = open(abs_path, 'r')
        for line in content.readlines():
            line = line.strip()
            self.stop_words.add(line)

    def extract_tags(self, *args, **kwargs):
        raise NotADirectoryError


class IDFLoader(object):

    def __init__(self, idf_path=None):
        self.path = ""
        self.idf_freq = {}
        self.median_idf = 0
        if idf_path:
            self.set_new_path(idf_path)

    def set_new_path(self, new_idf_path):
        if self.path != new_idf_path:
            self.path = new_idf_path
            content = open(new_idf_path, 'r')
            for line in content.readlines():
                word, freq = line.strip().split(" ")
                self.idf_freq[word] = float(freq)
            self.median_idf = sorted(
                self.idf_freq.values())[len(self.idf_freq) // 2]

    def get_idf(self):
        return self.idf_freq, self.median_idf


class TfIdf(KeywordExtractor):

    def __init__(self, idf_path=None):
        """

        :param idf_path:
        """
        self.tokenizer = None
        self.stop_words = self.STOP_WORDS.copy()
        self.idf_loader = IDFLoader(idf_path or DEFAULT_PATH)
        self.idf_freq, self.median_idf = self.idf_loader.get_idf()

    def set_idf_path(self, idf_path):
        new_abs_path = _get_abs_path(idf_path)
        if not os.path.isfile(new_abs_path):
            raise Exception("file does not exist: " + new_abs_path)
        self.idf_loader.set_new_path(new_abs_path)
        self.idf_freq, self.median_idf = self.idf_loader.get_idf()

    def list_2_pair(self, words):
        try:
            for w in words:
                wp = w.split("/")
                yield Pair(wp[0], wp[1])
        except:
            pass

    def extract_tags(self, sentence, option, top_k=20, with_weight=False, allow_pos=(), with_flag=False):
        """
        Extract keywords from sentence use tf-idf algorithm
        :param sentence:
        :param option: mecab tagger long option e.g. -d /home/ubuntu/Documents/final_binary_data/ -O pos
        :param top_k: return top_k number keywords.
        :param with_weight: if True, return a list of (word, weight);
                            if False, return a list of words.
        :param allow_pos: the allowed POS list e.g. ['ns' , 'n', 'vn', 'v', 'nr'].
                        if the POS of w is not in this list, it will be filtered.
        :param with_flag: only work with allow_pos is not empty.
                          if True, return a list of pair(word, weight) like pos.
                          if False, return a list of words.
        :return:
        """
        self.tokenizer = Tagger(option)
        if allow_pos and "pos" in option:
            allow_pos = frozenset(allow_pos)
            words = self.list_2_pair(self.tokenizer.parse(sentence).replace("\n", "").split())
        else:
            words = self.tokenizer.parse(sentence).replace("\n", "").split()
        freq = {}
        for w in words:
            if allow_pos:
                if w.flag not in allow_pos:
                    continue
                elif not with_flag:
                    w = w.word
            wc = w.word if allow_pos and with_flag else w
            if len(wc.strip()) < 2 or wc.lower() in self.stop_words:
                continue
            freq[w] = freq.get(w, 0) + 1
        total = sum(freq.values())
        for k in freq:
            kw = k.word if allow_pos and with_flag else k
            freq[k] *= self.idf_freq.get(kw, self.median_idf) / total

        if with_weight:
            tags = sorted(freq.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(freq, key=freq.__getitem__, reverse=True)
        if top_k:
            return tags[:top_k]
        else:
            return tags


