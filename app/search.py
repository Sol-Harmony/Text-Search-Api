import numpy as np

def build_vocabulary(tfidf_docs):

    vocab = set()

    for doc in tfidf_docs:
        vocab.update(doc.keys())

    return list(vocab)


def vectorize(doc, vocab):

    vector = []

    for word in vocab:
        vector.append(doc.get(word, 0))

    return np.array(vector)


def cosine_similarity(vec1, vec2):

    dot   = np.dot(vec1, vec2)

    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot / (norm1 * norm2)


def search(query_tfidf, docs_tfidf, top_k=3):

    vocab       = build_vocabulary(docs_tfidf)
    query_vec   = vectorize(query_tfidf, vocab)
    scores      = []

    for doc in docs_tfidf:
        doc_vec   = vectorize(doc, vocab)
        score     = cosine_similarity(query_vec, doc_vec)
        scores.append(score)

    ranked = sorted(
        list(enumerate(scores)),
        key       = lambda x: x[1],
        reverse   = True
    )

    return ranked[:top_k]