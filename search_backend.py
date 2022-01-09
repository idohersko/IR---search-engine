import math

import numpy as np
from collections import Counter, OrderedDict, defaultdict
from contextlib import closing
from inverted_index import *

TUPLE_SIZE = 6
TF_MASK = 2 ** 16 - 1 # Masking the 16 low bits of an integer


def read_posting_list(inverted, w):
  with closing(MultiFileReader()) as reader:
    locs = inverted.posting_locs[w]
    b = reader.read(locs, inverted.df[w] * TUPLE_SIZE)
    posting_list = []
    for i in range(inverted.df[w]):
      doc_id = int.from_bytes(b[i*TUPLE_SIZE:i*TUPLE_SIZE+4], 'big')
      tf = int.from_bytes(b[i*TUPLE_SIZE+4:(i+1)*TUPLE_SIZE], 'big')
      posting_list.append((doc_id, tf))
    return posting_list

def binary_search(query_to_search,index):
    #counter, each key will hold a number, this number will be the amount of word that hold this doc.
    counter = Counter([])
    #iterate over all the unique term of a quey
    for term in np.unique(query_to_search):
        try:
            #for each query take the posting list of the term
            list_of_doc = read_posting_list(index, term)
            #for each doc update the counter
            for doc_id,freq in list_of_doc:
                counter.update([doc_id])
        except:
            continue
    keys = (counter.most_common()).keys()
    return list(keys)

def iter_over_relevant_terms(query_to_search,index):
    candidates_list = set()
    candidates = {}
    N = len(dl_dict)
    for term in np.unique(query_to_search):
        try:
            normlized_tfidf=[]
            list_of_doc = read_posting_list(index, term)
            for doc_id,freq in list_of_doc:
                candidates_list.add(doc_id)
                normlized_tfidf.append((doc_id,(freq/dl_dict[doc_id][0])*math.log(N/index.df[term],10)))
            for doc_id,tfidf in normlized_tfidf:
                candidates[(doc_id,term)] = candidates.get((doc_id,term), 0) + tfidf
        except:
            continue
    return list(candidates_list),candidates

def cosine_similarity( query_to_search, index):
    dicti = {}
    candidates_docs_list,candidates_tfidf_dict = iter_over_relevant_terms(query_to_search,index)
    for doc in candidates_docs_list:
        mone = 0.0
        for term in np.unique(query_to_search):
            try:
                mone+=candidates_tfidf_dict[(doc,term)]
            except:
                continue
        mahane = float(dl_dict[doc][1])*math.sqrt(len(query_to_search)) #todo:documents tfidf_dict is taken from disk's memory
        dicti[doc] = mone/mahane
    return dicti

def get_top_n_docs(dicti,n=100):
    lst = sorted([(doc_id, score) for doc_id, score in dicti.items()], key = lambda x: x[1], reverse=True)[:n]
    return ([doc_id for doc_id, score in lst])


def cosine_sim_search(query_to_search,index):
    temp = cosine_similarity(query_to_search, index)
    top_n = get_top_n_docs(temp, 100)
    return top_n

