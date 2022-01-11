import math
from itertools import chain
import time
import builtins

import numpy as np

from inverted_index_gcp import *




# When preprocessing the data have a dictionary of document length for each document saved in a variable called `DL`.
class BM25_from_index:
    def __init__(self, index, dl_dict, index_name, k1=1.5, b=0.75):
        self.b = b
        self.k1 = k1
        self.dl_dict = dl_dict
        self.index = index
        self.index_name = index_name
        self.N = len(self.dl_dict)
        self.AVGDL = builtins.sum(self.dl_dict.values()) / self.N

    def get_candidate_documents(self, query_to_search, term_frequencies):
        candidates = []
        for term in np.unique(query_to_search):
            if term in self.index.df.keys():
                pls = term_frequencies[term].keys()
                candidates += pls
        return np.unique(candidates)

    def _score(self, query, doc_id, term_frequencies):

        score = 0.0
        doc_len = self.dl_dict[doc_id]
        for term in query:
            if term in self.index.df.keys():
                print()
                # term_frequencies = dict(backend.read_posting_list(self.index,term, self.index_name))
                if doc_id in term_frequencies[term].keys():
                    freq = term_frequencies[term][doc_id]
                    numerator = self.idf[term] * freq * (self.k1 + 1)
                    denominator = freq + self.k1 * (1 - self.b + self.b * doc_len / self.AVGDL)
                    score += (numerator / denominator)
        return score

    def search(self, query, N=100):
        idf = {}
        # all_terms =set()
        term_frequencies={}
        for term in query:
            if term in self.index.df.keys():
                term_frequencies[term] = dict(self.read_posting_list(self.index, term, self.index_name))
                # all_terms.add(term)
                n_ti = self.index.df[term]
                idf[term] = math.log(1 + (self.N - n_ti + 0.5) / (n_ti + 0.5))
            else:
                pass
        self.idf = idf

        all_can = self.get_candidate_documents(query, term_frequencies)
        score_doc = []
        for cand in all_can:
            score_doc.append((cand, self._score(query, cand, term_frequencies)))
        score_doc = sorted(score_doc, key=lambda x: -x[1])[:N]

        return score_doc


    def read_posting_list(self, inverted, w, index_name):
        with closing(MultiFileReader()) as reader:
            locs = inverted.posting_locs[w]
            b = reader.read(locs, inverted.df[w] * TUPLE_SIZE,
                            index_name)  # for the index_body give '', for the index title give '_title', for the index_anchor give "_anchor".
            posting_list = []
            for i in range(inverted.df[w]):
                doc_id = int.from_bytes(b[i * TUPLE_SIZE:i * TUPLE_SIZE + 4], 'big')
                tf = int.from_bytes(b[i * TUPLE_SIZE + 4:(i + 1) * TUPLE_SIZE], 'big')
                posting_list.append((doc_id, tf))
            return posting_list
