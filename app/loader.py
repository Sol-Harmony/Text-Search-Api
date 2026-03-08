def load_documents(path: str) -> list[str]:
    documents = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                documents.append(line)

    return documents