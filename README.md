# Wikipedia Search Engine

This project implements a search engine for the entire Wikipedia corpus, developed as part of a Data Retrieval course. The search engine processes queries and retrieves relevant documents using a combination of ranking algorithms.

## Project Overview

The search engine is designed to handle queries through a web interface, leveraging various data structures and algorithms to retrieve and rank documents from the Wikipedia corpus.

### Main Components

- **Backend.py**: Contains the `Backend` class, which initializes all preprocessing files and implements the core functions required to retrieve relevant documents.
- **search_frontend.py**: The main script that runs the search engine, providing various search functions. The primary search function merges three ranking methods: cosine similarity on the body, PageRank, and PageView.
- **BM25_from_index.py**: Implements the functions necessary for calculating the BM25 algorithm, a probabilistic information retrieval model.
- **inverted_index_gcp.py**: Provides a class for creating and reading the inverted indexes used by the search engine.

### Preprocessing

Before the search engine is operational, several indexes and dictionaries are precomputed:

- **Indexes**:
  - **Body Index**
  - **Title Index**
  - **Anchor Text Index**
  
- **Dictionaries**:
  - Document vector sizes and lengths
  - PageRank values
  - PageView counts
  - BM25 parameters for Body and Title

## Method Overview

The search engine operates using a series of carefully designed methods and processes:

1. **Query Handling**:
    - A query is submitted through a URL, which includes the IP of the virtual machine hosting the search engine.
    - The `search_frontend.py` file handles the initial reception of the query.
  
2. **Query Processing**:
    - The query is passed to the `Backend.py` file, where it is processed to determine the most relevant documents.
    - The `Backend` class initializes all necessary preprocessing files, including indexes and dictionaries.
    - It utilizes multiple functions to analyze the query and match it against the indexed Wikipedia documents.

3. **Document Retrieval**:
    - The search engine combines several ranking methods to retrieve and rank documents:
        - **Cosine Similarity** on the document body.
        - **PageRank** to assess the importance of documents.
        - **PageView** to evaluate the popularity of documents.
    - These methods are integrated within the search functions in `search_frontend.py`.

4. **BM25 Calculation**:
    - The `BM25_from_index.py` file contains the functions needed to compute the BM25 ranking score, which is an essential part of the document ranking process.

5. **Inverted Index Management**:
    - The `inverted_index_gcp.py` file defines the class used to create and read the inverted indexes.
    - The engine relies on these indexes to efficiently retrieve documents relevant to the query.

6. **Response Handling**:
    - Once the relevant documents are identified, the results are sent back to the user via the `search_frontend.py` file.

## Installation

To run the search engine locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/IR---search-engine.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd IR---search-engine
    ```
3. **Install dependencies**:
    Ensure that you have all required Python packages installed. You can use `pip` to install the dependencies listed in your environment or requirements file.

    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Search Engine**:
    You can start the search engine by running the `search_frontend.py` file:

    ```bash
    python search_frontend.py
    ```

## Usage

### Querying the Search Engine

- The engine accepts queries via a URL containing the IP of the virtual machine hosting the engine.
- The query is processed in the `Backend.py` file, and relevant documents are retrieved and ranked.
- The response is sent back to the user through the `search_frontend.py` file.

### Ranking Methods

The search engine combines three ranking methods to determine the relevance of documents:
1. **Cosine Similarity** on the document body.
2. **PageRank**: Ranks documents based on their importance within the Wikipedia corpus.
3. **PageView**: Uses the number of page views to assess the popularity of a document.

### BM25 Algorithm

The BM25 algorithm is used to rank documents based on probabilistic information retrieval principles, considering term frequency and document length.

