import logging
logger = logging.getLogger(__name__)

def load_documents(path: str) -> list[str]:
    documents = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    documents.append(line)

    except FileNotFoundError:
        logger.error(f"Datei nicht gefunden: {path}")
        raise RuntimeError(f"Datei nicht gefunden: {path}")

    except Exception as e:
        raise RuntimeError(f"Fehler beim Laden der Dokumente: {str(e)}")

    return documents