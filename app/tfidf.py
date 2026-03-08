from collections import Counter
import math

def term_frequency(tokens: list[str]) -> dict:
    return Counter(tokens)

def compute_tf(tokenized_documents: list[list[str]]) -> list[dict]:

    tf_list = []

    for tokens in tokenized_documents:
        tf = term_frequency(tokens)
        tf_list.append(tf)

    return tf_list


def compute_idf(tokenized_documents: list[list[str]]) -> dict:

    total_docs = len(tokenized_documents)

    word_document_count = {}

    for tokens in tokenized_documents:
        unique_words = set(tokens)

        for word in unique_words:
            word_document_count[word] = word_document_count.get(word, 0) + 1

    idf = {}

    for word, count in word_document_count.items():
        idf[word] = math.log(total_docs / count)

    return idf

def compute_tfidf(tf_list: list[dict], idf: dict) -> list[dict]:

    tfidf_documents = []

    for tf in tf_list:

        tfidf_doc = {}

        for word, freq in tf.items():

            tfidf_doc[word] = freq * idf.get(word, 0)

        tfidf_documents.append(tfidf_doc)

    return tfidf_documents