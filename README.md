# IR---search-engine
Search Engine on the entire Wikipedia corpus :
Wikipedia Search Engine for Data Retrieval Course.

A few words on funcionality of the code:
A query is given using an Url which holds the IP of the instance for the virtual machine that holds our engine, through the search_frontend. Then, the query is beeing sent to the Backend file for the computation of the relevant documents for this query, then, The response is going back to the user through the search_frontend file. 

Backend file:
This file holds the class Backend. This class initialize all the files of the preprocessing part of the engine. This class also holds all the function we need to retrieve the relevant documents.

search_frontend file:
This is the main file that runs our engine, all the functions that the user can call.
In this file, you can find a few search function, one of them is the main function of the engine, which is the search function : In order to search the relevant documents, we merged 3 ranking functionality : cosine similarity on the BODY, pagerank and pageview.    

BM25 file :
This file contains all the relevant function for the BM25 algorithm calculation.

inverted_index_gcp file :
Class we used to create the different inverted index we used. This class was also used in reading those indexes.


Preprocessing part : 
we are using 3 indexes that we calculated before the engine is mounted : Index Body.
                                                                         Index Title.
                                                                         Index Anchor.
we are also using 5 dictionnary : dictionnary that holds the size of the vector of each document ( and his lenghth)
                                  dictionnary of pagerank
                                  dictionnary of pageview
                                  2 dictionnaries for BM25 ( Body and Title)

