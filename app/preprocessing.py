import re

STOPWORDS = {
    "der","die","das","ein","eine","und","oder",
    "ist","im","in","am","an","zu","für","mit",
    "von","auf","den","dem","des"
}

def tokenize(text: str) -> list[str]:

    # alles klein
    text = text.lower()

    # Satzzeichen entfernen
    text = re.sub(r"[^\w\s]", "", text)

    # Wörter splitten
    tokens = text.split()

    # Stopwörter entfernen
    tokens = [word for word in tokens if word not in STOPWORDS]

    return tokens