from fastapi import FastAPI             #FastAPI wird verwendet, um eine REST-API zu erstellen
from contextlib import asynccontextmanager

from app.loader import load_documents
from app.preprocessing import tokenize
from app.tfidf import compute_tf, compute_idf, compute_tfidf
from app.search import search

from fastapi import HTTPException       #Exception Handling
import logging                          #logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
documents          = []
tokenized_docs     = []
tf_values          = []
idf_values         = {}
tfidf_values       = []

# Asynchroner Code, der beim Starten des Programms ausgeführt wird
@asynccontextmanager
async def lifespan(app: FastAPI):
    global documents, tokenized_docs, tf_values, idf_values, tfidf_values
    
    try:
        # Dokumente laden
        documents      = load_documents("data/documents.txt")
        # Tokenisierung
        tokenized_docs = [tokenize(doc) for doc in documents]
        # TF
        tf_values      = compute_tf(tokenized_docs)
        # IDF
        idf_values     = compute_idf(tokenized_docs)
        # TF-IDF
        tfidf_values   = compute_tfidf(tf_values, idf_values)

        logger.info(f"Dokumente geladen: {len(documents)}")
        logger.info("TF-IDF Index erstellt")

    except Exception as e:
        logger.error(f"Fehler beim Start: {e}")
        raise

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
    logger.info(f"Suchanfrage erhalten: '{q}' mit k={k}")
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query darf nicht leer sein")

    if k <= 0:
        raise HTTPException(status_code=400, detail="k muss größer als 0 sein")

    if not documents:
        raise HTTPException(status_code=500, detail="Keine Dokumente geladen")

    try:
        k = min(k, 10)
        tokens = tokenize(q)

        if not tokens:
            raise HTTPException(
                status_code=400,
                detail="Suchanfrage enthaelt nur Stopwoerter oder ungueltige Begriffe"
            )

        tf_query    = compute_tf([tokens])[0]
        tfidf_query = compute_tfidf([tf_query], idf_values)[0]

        results = search(tfidf_query, tfidf_values)

        answers = []
        for index, score in results[:k]:
            answers.append({
                "text": documents[index],
                "score": score
            })
            
        logger.info(f"{len(answers)} Ergebnisse zurueckgegeben")
        
        return {
            "query": q,
            "top_k": k,
            "results": answers
        }

    except HTTPException:
        raise  

    except Exception as e:
        logger.error(f"Fehler bei Suche: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Interner Fehler: {str(e)}"
        )