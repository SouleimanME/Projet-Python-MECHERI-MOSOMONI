import pandas as pd

from Author import Author
from Document import Document


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        doc_id = self.ndoc
        self.id2doc[doc_id] = doc
        self.ndoc += 1
        if doc.auteur not in self.authors:
            self.authors[doc.auteur] = Author(doc.auteur)
            self.naut += 1
        self.authors[doc.auteur].add(doc_id, doc)

    def show_par_date(self, n):
        docs = sorted(self.id2doc.values(), key=lambda d: d.date, reverse=True)
        for doc in docs[:n]:
            print(doc.date.date(), doc)

    def show_par_titre(self, n):
        docs = sorted(self.id2doc.values(), key=lambda d: d.titre.lower())
        for doc in docs[:n]:
            print(doc)

    def __repr__(self):
        return f"Corpus {self.nom} : {self.ndoc} documents, {self.naut} auteurs"

    def save(self, chemin):
        lignes = [{"id": i, "titre": d.titre, "auteur": d.auteur, "date": d.date,
                   "url": d.url, "texte": d.texte, "origine": d.origine}
                  for i, d in self.id2doc.items()]
        pd.DataFrame(lignes).to_csv(chemin, sep="\t", index=False)

    def load(self, chemin):
        df = pd.read_csv(chemin, sep="\t", dtype=str, keep_default_na=False)
        for _, ligne in df.iterrows():
            self.add(Document(ligne["titre"], ligne["auteur"], ligne["date"],
                              ligne["url"], ligne["texte"], ligne["origine"]))
