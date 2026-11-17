import html
import json
import re
import urllib.parse
import urllib.request

import pandas as pd
import xmltodict


def nettoyer(texte):
    texte = re.sub(r"<[^>]+>", " ", html.unescape(texte or ""))
    return " ".join(texte.split())


def lire_hackernews(donnees):
    docs = []
    for hit in donnees["hits"]:
        titre = nettoyer(hit["title"])
        docs.append({"titre": titre,
                     "auteur": hit["author"],
                     "date": hit["created_at"],
                     "url": hit.get("url") or "https://news.ycombinator.com/item?id=" + hit["objectID"],
                     "texte": nettoyer(hit.get("story_text")) or titre,
                     "origine": "hackernews"})
    return docs


def lire_arxiv(texte_xml):
    entrees = xmltodict.parse(texte_xml)["feed"].get("entry", [])
    if isinstance(entrees, dict):
        entrees = [entrees]
    docs = []
    for entree in entrees:
        auteurs = entree["author"]
        if isinstance(auteurs, list):
            auteurs = auteurs[0]
        docs.append({"titre": nettoyer(entree["title"]),
                     "auteur": auteurs["name"],
                     "date": entree["published"],
                     "url": entree["id"],
                     "texte": nettoyer(entree["summary"]),
                     "origine": "arxiv"})
    return docs


def collecter(theme, nombre):
    url = "https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(
        {"query": theme, "tags": "story", "hitsPerPage": nombre})
    with urllib.request.urlopen(url) as reponse:
        docs = lire_hackernews(json.load(reponse))

    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": "all:" + theme, "start": 0, "max_results": nombre})
    with urllib.request.urlopen(url) as reponse:
        docs += lire_arxiv(reponse.read())

    df = pd.DataFrame(docs)
    df = df[df["texte"].str.len() >= 20]
    df.insert(0, "id", range(len(df)))
    return df
