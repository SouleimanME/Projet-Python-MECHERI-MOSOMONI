import os

import collecte
from Corpus import Corpus

DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER = os.path.join(DOSSIER, "data", "corpus.csv")
THEME = "climate"

MENU = """
1. Infos sur le corpus
2. Documents triés par date
3. Documents triés par titre
4. Afficher un document
5. Statistiques d'un auteur
6. Sauvegarder puis recharger le corpus
0. Quitter"""


def infos(corpus):
    textes = [d.texte for d in corpus.id2doc.values()]
    mots = sum(len(t.split(" ")) for t in textes) / len(textes)
    phrases = sum(len(t.split(".")) for t in textes) / len(textes)
    print(corpus)
    print(f"En moyenne {mots:.0f} mots et {phrases:.1f} phrases par document")
    print("Taille de tous les textes réunis :", len(" ".join(textes)), "caractères")


def stats_auteur(corpus):
    nom = input("Nom de l'auteur : ").strip()
    if nom not in corpus.authors:
        print("Auteur inconnu")
        return
    auteur = corpus.authors[nom]
    print(auteur)
    print(f"Taille moyenne : {auteur.taille_moyenne():.0f} mots")
    for doc in auteur.production.values():
        print("-", doc)


def afficher_document(corpus):
    choix = input(f"Numéro du document (0 à {corpus.ndoc - 1}) : ").strip()
    if choix.isdigit() and int(choix) in corpus.id2doc:
        corpus.id2doc[int(choix)].afficher()
    else:
        print("Numéro invalide")


def sauvegarder_recharger(corpus):
    chemin = os.path.join(DOSSIER, "data", "copie.csv")
    corpus.save(chemin)
    copie = Corpus(corpus.nom)
    copie.load(chemin)
    os.remove(chemin)
    print("Rechargé :", copie)


def main():
    if not os.path.exists(FICHIER):
        print("Téléchargement des documents...")
        collecte.collecter(THEME, 100).to_csv(FICHIER, sep="\t", index=False)
    corpus = Corpus(THEME)
    corpus.load(FICHIER)

    while True:
        print(MENU)
        match input("Choix : ").strip():
            case "1":
                infos(corpus)
            case "2":
                corpus.show_par_date(10)
            case "3":
                corpus.show_par_titre(10)
            case "4":
                afficher_document(corpus)
            case "5":
                stats_auteur(corpus)
            case "6":
                sauvegarder_recharger(corpus)
            case "0":
                break
            case _:
                print("Choix invalide")


if __name__ == "__main__":
    main()
