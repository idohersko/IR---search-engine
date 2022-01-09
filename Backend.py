import math

import numpy as np
from collections import Counter, OrderedDict, defaultdict
from contextlib import closing

from google.cloud import storage

from inverted_index import *


class Backend:
    size_vec_len_dict = 0
    index_body = None
    index_title = None
    index_anchor = None
    # dictionnary of {Key : docID, Value : (tfidf vector size, doc. len)}
    vec_len_dict = None
    # dictionnary of PageView of {Key : docID, Value : Page view score}
    page_view_dict = None
    # dictionnary of PageView of {Key : docID, Value : Page rank score}
    page_rank_dict = None

    # more parameters
    TUPLE_SIZE = 6
    TF_MASK = 2 ** 16 - 1  # Masking the 16 low bits of an integer

    def __init__(self):
        bucket_name = "ass-3-bucket-tamar"
        client = storage.Client()
        blobs = client.list_blobs(bucket_name)
        #connect to the bucket and read the relevant files.
        for blob in blobs:
            if blob.name == 'postings_gcp/index.pkl':
                with blob.open("rb") as f:
                    self.index_body = pickle.load(f)
            elif blob.name == 'postings_gcp_anchor/index.pkl':
                with blob.open("rb") as f:
                    self.index_anchor = pickle.load(f)
            elif blob.name == 'postings_gcp_title/index.pkl':
                with blob.open("rb") as f:
                    self.index_title = pickle.load(f)
            elif blob.name == 'page_view_dict.pkl':
                with blob.open("rb") as f:
                    self.page_view_dict = pickle.load(f)
            elif blob.name == 'pagerank_dict.pkl':
                with blob.open("rb") as f:
                    self.page_rank_dict = pickle.load(f)

        self.size_vec_len_dict = len(self.vec_len_dict)

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

    def binary_search(self, query_to_search, index, index_name):
        # counter, each key will hold a number, this number will be the amount of word that hold this doc.
        counter = Counter([])
        # iterate over all the unique term of a query
        for term in np.unique(query_to_search):
            try:
                # for each query take the posting list of the term
                list_of_doc = self.read_posting_list(index, term, index_name)
                # for each doc update the counter
                for doc_id, freq in list_of_doc:
                    counter.update([doc_id])
            except:
                continue
        # sort by the most common items and return only the keys
        keys = dict((counter.most_common())).keys()
        return list(keys)

    # This function iterate over the terms of a query and calculate the size of vector of the query and also returns 2 other parameters : the list of candidates document (which later we will give a score for them), the
    def iter_over_relevant_terms(self, query_to_search, index, index_name):
        candidates_list = set()
        candidates = {}
        query_vec = 0
        query_tf_counter = Counter(query_to_search)
        for term in np.unique(query_to_search):
            try:
                if term in index.df.keys():
                    tf_term = query_tf_counter[term]/len(query_to_search)
                    idf_term =math.log10(self.size_vec_len_dict/index.df[term])
                    query_vec += (idf_term * tf_term) ** 2
                    normlized_tfidf = []
                    list_of_doc = self.read_posting_list(index, term, index_name)
                    for doc_id, freq in list_of_doc:
                        candidates_list.add(doc_id)
                        normlized_tfidf.append((doc_id, (freq / self.vec_len_dict[doc_id][0]) * math.log(
                            self.size_vec_len_dict / index.df[term], 10)))
                    for doc_id, tfidf in normlized_tfidf:
                        candidates[(doc_id, term)] = candidates.get((doc_id, term), 0) + tfidf
            except:
                continue
        return list(candidates_list), candidates, math.sqrt(query_vec)

    def cosine_similarity(self, query_to_search, index, index_name):
        dicti = {}
        candidates_docs_list, candidates_tfidf_dict, query_vec = self.iter_over_relevant_terms(query_to_search, index, index_name)
        for doc in candidates_docs_list:
            mone = 0.0

            for term in np.unique(query_to_search):
                if (doc, term) in candidates_tfidf_dict.keys():
                    mone += candidates_tfidf_dict[(doc, term)]
            mahane = float(self.vec_len_dict[doc][1]) * query_vec
            dicti[doc] = mone / mahane
        return dicti

    def get_top_n_docs(self, dicti, n=100):
        lst = sorted([(doc_id, score) for doc_id, score in dicti.items()], key=lambda x: x[1], reverse=True)[:n]
        return ([doc_id for doc_id, score in lst])

    def cosine_sim_search(self, query_to_search, index, index_name):
        temp = self.cosine_similarity(query_to_search, index, index_name)
        top_n = self.get_top_n_docs(temp)
        return top_n

    #returns dictionnary values of a given list of docs
    def get_score_for_doc_from_dicti(self, lists_of_documents, dicti):
        page_views = []
        for docID in lists_of_documents:
            page_views.append(dicti[docID])
        return page_views


#todo check if numpy is good or bad for speed