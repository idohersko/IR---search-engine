import numpy as np
from collections import Counter, OrderedDict, defaultdict
from inverted_index import *


def search_query_in_anchor(query_to_search,index):
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