from fastapi import FastAPI             #FastAPI wird verwendet, um eine REST-API zu erstellen
from contextlib import asynccontextmanager

from app.loader import load_documents
from app.preprocessing import tokenize
from app.tfidf import compute_tf, compute_idf, compute_tfidf
from app.search import search

documents          = []
tokenized_docs     = []
tf_values          = []
idf_values         = {}
tfidf_values       = []

# Asynchroner Code, der beim Starten des Programms ausgeführt wird
@asynccontextmanager
async def lifespan(app    : FastAPI):
    global documents, tokenized_docs, tf_values, idf_values, tfidf_values
    # Dokumente laden
    documents      = load_documents("data/documents.txt")
    # Alle Dokumente tokenisieren (Text in einzelne Wörter zerlegen)
    tokenized_docs = [tokenize(doc) for doc in documents]
    # Term Frequency für jedes Dokument berechnen (Wie oft kommt ein Wort im jeweiligen Dokument vor)
    tf_values      = compute_tf(tokenized_docs)
    # Inverse Document Frequency berechnen (Wie selten ein Wort im gesamten Dokumentensatz ist)
    idf_values     = compute_idf(tokenized_docs)
    # TF-IDF Werte berechnen. Kombination aus Wort-Häufigkeit und Seltenheit
    tfidf_values   = compute_tfidf(tf_values, idf_values)

    print("Dokumente geladen:", len(documents))
    print("TF-IDF Index erstellt")
    yield

# Initialisierung der FastAPI Anwendung und die benötigten Variablen
app                = FastAPI(lifespan=lifespan)

# Root-Endpunkt zum Testen, ob die API läuft
@app.get("/")
def root():
    return {"message": "Text Search API laeuft"}

# Gibt alle geladenen Dokumente zurück
@app.get("/documents")
def get_documents():
    return {"documents": documents}

# Gibt die tokenisierten Dokumente zurück (Dokumente als Liste von Wörtern)
@app.get("/tokens")
def get_tokens():
    return {"tokens": tokenized_docs}

# Gibt die Term Frequency Werte zurück (Wort-Häufigkeiten pro Dokument)
@app.get("/tf")
def get_tf():
    return {"tf": tf_values}

# API-Endpunkt zum Anzeigen der IDF-Werte
@app.get("/idf")
def get_idf():
    return {"idf": idf_values}

# API-Endpunkt zum Anzeigen der TF-IDF Werte
@app.get("/tfidf")
def get_tfidf():
    return {"tfidf": tfidf_values}

# Such-Endpunkt. K entscheidet, wie viele ergebnisse man haben wiil. Z.B /search?q=HIER FRAGE STELLEN&k=2
@app.get("/search")
def search_endpoint(q: str, k: int = 1):
    k             = min(k, 10)
    tokens        = tokenize(q)
    tf_query      = compute_tf([tokens])[0]
    tfidf_query   = compute_tfidf([tf_query], idf_values)[0]

    results = search(tfidf_query, tfidf_values)

    answers = []

    for index, score in results[:k]:
        answers.append({
            "text": documents[index],
            "score": score
        })

    return {
        "query": q,
        "top_k": k,
        "results": answers
    }