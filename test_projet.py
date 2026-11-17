import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime

import collecte
from Author import Author
from Corpus import Corpus
from Document import Document

XML_ARXIV = """<feed>
  <entry><id>http://arxiv.org/abs/1</id><published>2020-01-02T00:00:00Z</published>
    <title>Un titre
      sur deux lignes</title><summary>Un résumé.</summary>
    <author><name>A</name></author><author><name>B</name></author></entry>
</feed>"""


def petit_corpus():
    corpus = Corpus("test")
    corpus.add(Document("Bonjour", "alice", "2021-03-01T10:00:00Z", "u1", "Un deux trois. Quatre.", "hackernews"))
    corpus.add(Document("Arbre", "bob", "2022-06-15T08:30:00Z", "u2", "Un texte", "arxiv"))
    corpus.add(Document("Climat", "alice", "2020-01-10T12:00:00Z", "u3", "Un", "hackernews"))
    return corpus


class CollecteTest(unittest.TestCase):

    def test_nettoyer(self):
        self.assertEqual("a'b c", collecte.nettoyer("<p>a&#x27;b\n<i>c</i>"))

    def test_lire_hackernews(self):
        donnees = {"hits": [{"objectID": "7", "title": "Titre", "author": "bob",
                             "created_at": "2023-01-01T10:00:00Z", "url": None,
                             "story_text": None}]}
        doc = collecte.lire_hackernews(donnees)[0]
        self.assertEqual("Titre", doc["texte"])
        self.assertEqual("https://news.ycombinator.com/item?id=7", doc["url"])

    def test_lire_arxiv(self):
        doc = collecte.lire_arxiv(XML_ARXIV)[0]
        self.assertEqual("Un titre sur deux lignes", doc["titre"])
        self.assertEqual("A", doc["auteur"])
        self.assertEqual("arxiv", doc["origine"])


class DocumentTest(unittest.TestCase):

    def test_date(self):
        doc = Document("T", "a", "2023-05-01T12:30:00Z", "u", "x")
        self.assertEqual(datetime(2023, 5, 1, 12, 30), doc.date)
        self.assertEqual("T", str(doc))

    def test_author(self):
        auteur = Author("alice")
        auteur.add(0, Document("T", "alice", None, "u", "un deux trois"))
        auteur.add(1, Document("T", "alice", None, "u", "un"))
        self.assertEqual(2, auteur.ndoc)
        self.assertEqual(2, auteur.taille_moyenne())


class CorpusTest(unittest.TestCase):

    def test_add(self):
        corpus = petit_corpus()
        self.assertEqual(3, corpus.ndoc)
        self.assertEqual(2, corpus.naut)
        self.assertEqual(2, corpus.authors["alice"].ndoc)
        self.assertEqual("Corpus test : 3 documents, 2 auteurs", repr(corpus))

    def test_tris(self):
        corpus = petit_corpus()
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            corpus.show_par_date(2)
            corpus.show_par_titre(1)
        self.assertEqual(["2022-06-15 Arbre", "2021-03-01 Bonjour", "Arbre"],
                         sortie.getvalue().splitlines())

    def test_save_load(self):
        corpus = petit_corpus()
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "corpus.csv")
            corpus.save(chemin)
            copie = Corpus("copie")
            copie.load(chemin)
        self.assertEqual(corpus.ndoc, copie.ndoc)
        for i, doc in corpus.id2doc.items():
            self.assertEqual(vars(doc), vars(copie.id2doc[i]))

    def test_donnees_du_depot(self):
        corpus = Corpus("climate")
        corpus.load(os.path.join(os.path.dirname(__file__), "data", "corpus.csv"))
        self.assertGreater(corpus.ndoc, 100)
        self.assertTrue(all(len(d.texte) >= 20 for d in corpus.id2doc.values()))


if __name__ == "__main__":
    unittest.main()
