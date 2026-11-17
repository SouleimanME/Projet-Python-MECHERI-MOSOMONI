# Projet Python : corpus Hacker News et Arxiv

Projet de Programmation de spécialité (Python), 2026-2027.
Binôme : MECHERI Souleiman (2232870) et MOSOMONI Jason (2223042).

Version 1 (tag `v1`, TD 3 et 4) : on récupère des documents sur le thème « climate »
depuis Hacker News et Arxiv, puis on les range dans des objets `Document`, `Author`
et `Corpus` qu'on explore depuis un menu texte.

Le rapport se trouve dans `rapport/rapport.pdf`.

## Installation

Python 3.10 ou plus récent :

```
pip install -r requirements.txt
```

## Utilisation

```
python main.py
```

Le corpus est lu dans `data/corpus.csv`. Si ce fichier n'existe pas, le programme
interroge les API puis le crée.

## Tests

```
python -m unittest -v
```

## Fichiers

```
main.py          menu texte
collecte.py      TD 3 : récupération des documents
Document.py      TD 4 : classe Document
Author.py        TD 4 : classe Author
Corpus.py        TD 4 : classe Corpus
test_projet.py   tests unitaires
data/corpus.csv  documents récupérés (séparés par des tabulations)
```
