class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}

    def add(self, doc_id, doc):
        self.production[doc_id] = doc
        self.ndoc += 1

    def taille_moyenne(self):
        return sum(len(d.texte.split()) for d in self.production.values()) / self.ndoc

    def __str__(self):
        return f"{self.name} ({self.ndoc} documents)"
