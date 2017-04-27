#!/usr/bin/env python
# encoding=utf-8

import sys
from operator import itemgetter
from collections import defaultdict
from .MeCab import Tagger
from .tfidf import KeywordExtractor
from .pair import Pair

itervalues = lambda d: iter(d.values())


class IndirectWeightedGraph(object):
    d = 0.85

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, start, end, weight):

        """use a tuple (start, end, weight) instead of a edge object"""
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    def rank(self):

        """sort for the candidate words"""
        ws = defaultdict(float)
        out_sum = defaultdict(int)

        ws_def = 1 / (len(self.graph) or 1)
        for n, out in self.graph.items():
            ws[n] = ws_def
            out_sum[n] = sum((e[2] for e in out), 0)

        sorted_keys = sorted(self.graph.keys())
        for x in range(10):
            for n in sorted_keys:
                s = 0
                for e in self.graph[n]:
                    s += e[2] / out_sum[e[1]] * ws[e[1]]
                ws[n] = (1 - self.d) + self.d * s

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in itervalues(ws):
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in ws.items():
            ws[n] = (w - min_rank / 10) / (max_rank - min_rank / 10)

        return ws


class TextRank(KeywordExtractor):

    def __init__(self):
        self.tokenizer = None
        self.stop_words = self.STOP_WORDS.copy()
        self.pos_filter = frozenset(('ns', 'n', 'vn', 'v'))
        self.window = None

    def pair_filter(self, wp):
        return (wp.flag in self.pos_filter and len(wp.word.strip()) >= 2
                and wp.word.lower() not in self.stop_words)

    def list2pair(self, words):
        try:
            for w in words:
                wp = w.split("/")
                yield Pair(wp[0], wp[1])
        except:
            pass

    def text_rank(self, sentence, option, window=5, top_k=20, with_weight=False, allow_pos=('ns', 'n', 'vn', 'v'), with_flag=False):
        """
        extract keywords from sentence using textrank algorithm
        :param sentence:
        :param option: mecab tagger long option e.g. -d /home/ubuntu/Documents/final_binary_data/ -O pos
        :param window: words co-occurrence windows size
        :param top_k: return top number keywords. 'None' for all possible words.
        :param with_weight: if True, return a list of (word, weight);
                            if False, return a list of words.
        :param allow_pos: the allowed POS list e.g. ['ns', 'n', 'vn', 'v'].
                          if the POS of w is not in this list, it will be filtered
        :param with_flag:if True, return a list of pair(word, weight);
                         if False, return a list of words.
        :return:
        """
        self.tokenizer = Tagger(option)
        self.window = window
        g = IndirectWeightedGraph()
        cm = defaultdict(int)
        words = tuple(self.list2pair(self.tokenizer.parse(sentence).replace("\n", "").split()))
        for i, wp in enumerate(words):
            if self.pair_filter(wp):
                for j in range(i + 1, i + self.window):
                    if j >= len(words):
                        break
                    if not self.pair_filter(words[j]):
                        continue
                    if allow_pos and with_flag:
                        cm[(wp, words[j])] += 1
                    else:
                        cm[(wp.word, words[j].word)] += 1

        for terms, w in cm.items():
            g.add_edge(terms[0], terms[1], w)

        nodes_rank = g.rank()
        if with_weight:
            tags = sorted(nodes_rank.items(), key=itemgetter(1), reverse=True)
        else:
            tags = sorted(nodes_rank, key=nodes_rank.__getitem__, reverse=True)

        if top_k:
            return tags[:top_k]
        else:
            return tags

    extract_tags = text_rank



