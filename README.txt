# Text Search API - Entwicklung einer Dokumentensuch-API auf Basis klassischer Textanalyse in Python

Github Repository: https://github.com/Sol-Harmony/Text-Search-Api

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

# Repository klonen:
git clone <repo-url>
cd <repo-ordner>
(Oder das Projekt runterladen und das Verzeichnis mit dem IDE öffnen)


# Virtuelle Umgebung erstellen
python -m venv .venv   # oder "python3 -m venv .venv" auf Linux/Mac

# Umgebung aktivieren
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux / Mac:
source .venv/bin/activate

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

Beim Start des Servers wird die Dokumentensammlung einmalig vorbereitet, um eine effiziente Suche zu ermöglichen:

1. Dokumente werden aus der Datei geladen
2. Die Texte werden tokenisiert (in einzelne Wörter zerlegt)
3. Eine Vorverarbeitung wird durchgeführt:
   - Umwandlung in Kleinbuchstaben
   - Entfernen von Stopwords (z. B. „und“, „der“, „die“)
4. Term-Frequency (TF) Werte werden für jedes Dokument berechnet
5. Inverse Document Frequency (IDF) Werte werden für den gesamten Dokumentensatz berechnet
6. Aus TF und IDF werden TF-IDF Vektoren erstellt

Diese vorberechneten Daten werden im Speicher gehalten, sodass Suchanfragen schnell verarbeitet werden können.

---

## Suchprozess

Bei einer Suchanfrage läuft folgender Ablauf ab:

1. Die Anfrage wird wie ein Dokument verarbeitet:
   - Tokenisierung
   - Stopword-Filterung
   - Umwandlung in einen TF-IDF Vektor

2. Der Anfrage-Vektor wird mit allen Dokument-Vektoren verglichen

3. Die Ähnlichkeit wird mithilfe der **Cosine Similarity** berechnet

4. Die Dokumente werden nach ihrer Ähnlichkeit sortiert

5. Die Top-k relevantesten Dokumente werden als Ergebnis zurückgegeben

---

## Fehlerbehandlung und Robustheit

Zur Verbesserung der Stabilität wurden zusätzliche Maßnahmen implementiert:

- Leere oder ungültige Suchanfragen werden abgefangen
- Fehler bei der Verarbeitung führen zu klaren HTTP-Fehlermeldungen
- Kritische Abschnitte der Anwendung sind durch Try-Except-Blöcke abgesichert

---

## Logging

Zur besseren Nachvollziehbarkeit verwendet das System das Python-Logging-Modul:

- Start des Servers und Laden der Dokumente werden protokolliert
- Suchanfragen werden erfasst
- Fehler und Ausnahmen werden geloggt

Dies erleichtert Debugging und Analyse des Systemverhaltens.
