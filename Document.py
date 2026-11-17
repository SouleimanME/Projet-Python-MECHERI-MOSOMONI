from datetime import datetime


class Document:
    def __init__(self, titre, auteur, date, url, texte, origine=""):
        self.titre = titre
        self.auteur = auteur
        if isinstance(date, str):
            date = datetime.fromisoformat(date[:19])
        self.date = date
        self.url = url
        self.texte = texte
        self.origine = origine

    def afficher(self):
        print("Titre :", self.titre)
        print("Auteur :", self.auteur)
        print("Date :", self.date)
        print("URL :", self.url)
        print("Origine :", self.origine)
        print("Texte :", self.texte)

    def __str__(self):
        return self.titre
