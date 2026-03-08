# Text Search API – Prototyp (Readme generiert mit ChatGPT und überprüft von Hamzah Mansor)

## Beschreibung

Dieses Projekt ist ein einfaches Beispiel eines Information-Retrieval-Systems.
Die Anwendung lädt eine Sammlung von Textdokumenten, verarbeitet diese und ermöglicht eine Suche nach relevanten Dokumenten über eine REST-API.

Die Implementierung basiert auf einem klassischen **TF-IDF Ansatz**:

1. Dokumente werden geladen
2. Texte werden tokenisiert (in Wörter zerlegt)
3. Term Frequency (TF) wird berechnet
4. Inverse Document Frequency (IDF) wird berechnet
5. TF-IDF Vektoren werden erstellt
6. Eine Anfrage wird mit den Dokumenten verglichen, um die relevantesten Ergebnisse zu finden

---
# Projektstruktur
```
project/
│
├── app/
│   ├── loader.py          # Laden der Dokumente
│   ├── preprocessing.py   # Tokenisierung
│   ├── tfidf.py           # TF, IDF und TF-IDF Berechnung
│   ├── search.py          # Ranking / Ähnlichkeitssuche
│
├── data/
│   └── documents.txt      # Beispieldokumente
│
├── main.py                # FastAPI Server
└── README.md
```

---
# Installation

Voraussetzungen:

* Python 3.10+
* pip

Repository klonen:


Abhängigkeiten installieren:

```
pip install numpy fastapi uvicorn
```

---
# Server starten
Der Server kann mit folgendem Befehl gestartet werden:
```
uvicorn main:app --reload
```

Danach läuft die API standardmäßig unter:
http://127.0.0.1:8000
```

---
# API testen
## 1. Root-Endpunkt
Testet, ob die API läuft.
```
http://127.0.0.1:8000/
```

Antwort:
```
{"message": "Text Search API laeuft"}
```

---
## 2. Dokumente anzeigen
```
/documents
```
Zeigt alle geladenen Dokumente.
---

## 3. Tokenisierte Dokumente
```
/tokens
```
Zeigt die Dokumente nach der Tokenisierung (Wortlisten).
---

## 4. TF Werte
```
/tf
```
Zeigt die Term-Frequency-Werte für alle Dokumente.
---

## 5. IDF Werte
```
/idf
```
Zeigt die berechneten Inverse-Document-Frequency-Werte.
---

## 6. TF-IDF Werte
```
/tfidf
```
Zeigt die finalen TF-IDF Vektoren der Dokumente.
---

## 7. Suche
Beispiel:
```
/search?q=python
```
oder
```
/search?q=python&k=3
```

Parameter:

| Parameter | Beschreibung          |
| --------- | --------------------- |
| q         | Suchanfrage           |
| k         | Anzahl der Ergebnisse |

Beispielantwort:
```
{
 "query": "python",
 "top_k": 3,
 "results": [
   {
     "text": "Python ist eine Programmiersprache...",
     "score": 0.82
   }
 ]
}
```

---
# Funktionsweise

Beim Start des Servers passiert Folgendes:

1. Dokumente werden aus der Datei geladen
2. Alle Dokumente werden tokenisiert
3. TF Werte werden berechnet
4. IDF Werte werden berechnet
5. TF-IDF Vektoren werden erstellt

Diese Schritte werden **nur einmal beim Start** durchgeführt, um die Performance zu verbessern.
---

# Aktueller Stand
Der Prototyp implementiert:

* Dokumentenimport
* Tokenisierung
* TF-IDF Berechnung
* Ranking von Dokumenten
* REST API zur Abfrage

Ziel ist es, die grundlegenden Konzepte von **Information Retrieval und Textsuche** zu demonstrieren.
---

# Mögliche Erweiterungen

Folgende Verbesserungen sind für die finale Version geplant bzw. möglich:

### Verbesserte Textverarbeitung
* Stopword-Filterung
* Normalisierung von Groß-/Kleinschreibung

### Verbesserte Suche
* Cosine Similarity für genaueres Ranking
* Gewichtung von Begriffen
* bessere Query-Verarbeitung

### Dokumentverarbeitung
* Aufteilung langer Dokumente in kleinere Textabschnitte (Chunks)
* Unterstützung mehrerer Dokumentdateien
* Upload neuer Dokumente über die API

### Erweiterte API
* Pagination für große Ergebnismengen
* Dokument-Metadaten
* Logging von Suchanfragen

### Erweiterte Suche
* semantische Suche mit Embeddings
* Integration eines Sprachmodells zur Antwortgenerierung
---
