from collections import defaultdict
from sklearn.cluster import AffinityPropagation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import re

from math import ceil
import json
import argparse
import numpy as np

import spacy
nlp = spacy.load('fr_core_news_lg')

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

parser = argparse.ArgumentParser(description = "fichier")
parser.add_argument("-v", "--verbose", help = "verbose mode", action = "store_true")
parser.add_argument("corpus", help = "path of json file")
parser.add_argument("window", help = "time window size (number of year)")
args = parser.parse_args()


def get_corpus(articles, window):
    """Récupération du corpus avec répartition des articles par année"""
        
    corpus = defaultdict(list)
        
    annees = []
    for articleid, article in articles.items():
        try:
            annee = article["date"].split()[-1]
        except:
            annee = article["date"][0].split()[-1]
        if annee != "inconnue":
            if window == "1":
                corpus[annee].append(articleid)
            else:
                annees.append(annee)
    
    if int(window) > 1:
        annees = sorted(list(set(annees)))
        windows = []
        i = int(annees[0])
        while i <= int(annees[-1]):
            j = i + int(window) -1
            windows.append("-".join([str(i), str(j)]))
            i = j+1
        for articleid, article in articles.items():
            try:
                annee = article["date"].split()[-1]
            except:
                annee = article["date"][0].split()[-1]
            if annee != "inconnue":
                time_window = [time_window for time_window in windows if time_window.split("-")[0] <= annee <= time_window.split("-")[1]][0]
                corpus[time_window].append(articleid)
        
        
    return corpus


def get_embeddings(corpus, articles):

    """Repésentation en word embeddings"""

    corpus_pretraite = {}
    for annee, articleids in corpus.items():
        data = [articles[id]['texte'] for id in articleids]
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]
        model = Doc2Vec(tagged_data, vector_size=5, window=2, min_count=1, workers=4)
        corpus_pretraite[annee] = [model.infer_vector(word_tokenize(doc.lower())) for doc in data]
    return corpus_pretraite


def get_cluster(corpus_pretraite):

    """Application du clustering"""

    clusterings = {}

    for annee, articles in corpus_pretraite.items():
        print("Clustering year ", annee)
        clustering = AffinityPropagation(random_state=5).fit(articles) #convergence_iter à 15 par défaut, modifier ?
        clusterings[annee] = list(clustering.labels_)
        print(len(set(clusterings[annee])), " clusters")
        
    return clusterings


def pretrait(texte):

    """Supprime stopwords, ponctuation et mot de moins de 3 lettres d'un texte"""
    
    texte = texte.lower()
    texte = re.sub("marie-claire", "", texte)
    texte = re.sub(r"[-\']", " ", texte)
    texte = re.sub(r"\s+", " ", texte)
    
    return " ".join([token.text for token in nlp(texte) if len(token.text) > 2 and token.lemma_ not in ("faire", "très", "avoir") and not token.is_stop and not token.is_digit and not token.is_punct and not token.is_space])


def get_lda(cluster_docs, annee, taille_ngrams):
    """Prend en entrée la liste des clusters (articles concaténés) d'une année
    Retourne pour chaque cluster les mots représentant les topics principaux (10 mots en tout)"""
    
    vectorizer = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b', ngram_range=(taille_ngrams,taille_ngrams))
    count_data = vectorizer.fit_transform(cluster_docs)
    lda = LDA(n_components=len(cluster_docs), n_jobs=-1)
    clusters_lda = lda.fit_transform(count_data)
    words = vectorizer.get_feature_names()

    clusters_topics = []
    for j, cluster in enumerate(clusters_lda):
        topics_words = []
        topics_index = cluster.argsort()[::-1]
        selected_topics = []
        i = prob = 0
        while prob <= 0.5 and len(selected_topics) < 10:
            selected_topics.append(topics_index[i])
            prob += cluster[topics_index[i]]
            i+=1

        terms_per_topic = ceil(10/len(selected_topics))
        for topic in selected_topics:
            for id_term in lda.components_[topic].argsort()[::-1]:
                if len(topics_words) == terms_per_topic:
                    break
                tokens = nlp(words[id_term])
                if words[id_term] not in topics_words and (taille_ngrams == 1 or not (len(tokens[0].text) <= 2 or tokens[0].lemma_ in ("faire", "très", "avoir") or tokens[0].is_stop or tokens[0].is_digit or tokens[0].is_punct or tokens[0].is_space or len(tokens[-1].text) <= 2 or tokens[-1].is_stop or tokens[-1].is_digit or tokens[-1].is_punct or tokens[-1].is_space)) :
                    topics_words.append(words[id_term])

        clusters_topics.append(topics_words)

    return clusters_topics


def print_clusters(corpus_path, window):
    """Visualisation des résultats"""

    with open(corpus_path) as file:
        articles = json.load(file)
    print(len(articles), " articles dans le corpus")
    corpus = get_corpus(articles, window)
    corpus_pretraite = get_embeddings(corpus, articles)
    clusterings = get_cluster(corpus_pretraite)
    output = {}
    output['corpus'] = corpus_path.split("/")[-1].split("_")[0]
    output['results'] = {}
    for annee, clusters in clusterings.items():
        print("Processing year ", annee)
        output['results'][annee] = []
        clusters_doc = []
        liste_articleid = []
        divers = []
        regroupement = False
        for cluster in set(clusters):
            indices = [i for i in range(len(clusters)) if clusters[i] == cluster]
            if len(indices) > 1:
                liste_articleid.append([corpus[annee][i] for i in indices])
                clusters_doc.append(" ".join([articles[i]['texte'] for i in liste_articleid[-1]]))
            else:
                divers.append(corpus[annee][indices[0]])
        if divers != []:
            liste_articleid.append(divers)
            clusters_doc.append(articles[liste_articleid[-1][0]]['texte'])
            regroupement = True
        clusters_topics = {}
        for taille_ngrams in range(1,4):
            if taille_ngrams == 1:
                clusters_topics[taille_ngrams] = get_lda([pretrait(doc) for doc in clusters_doc], annee, taille_ngrams)
            else:
                clusters_topics[taille_ngrams] = get_lda(clusters_doc, annee, taille_ngrams)
        i = 1
        for topics in clusters_topics[1]:
            cluster = {}
            if regroupement and i == len(clusters_topics):
                cluster['id'] = "Divers"
            else:
                cluster['id'] = str(i)
            cluster['1-grams'] = list(topics)
            cluster['2-grams'] = list(clusters_topics[2][i-1])
            cluster['3-grams'] = list(clusters_topics[3][i-1])
            cluster['articles'] = []
            for articleid in liste_articleid[i-1]:
                article = {}
                article['id'] = articleid
                article['titre'] = " ".join(articles[articleid]['texte'].split()[:6]) + "..."
                cluster['articles'].append(article)
            output['results'][annee].append(cluster)
            i +=1
    return output


results = print_clusters(args.corpus, args.window)
pathname = "clustered_data/" + args.corpus.split("/")[-1].split("_")[0] + "_" + args.window + ".json"
with open(pathname, 'w') as output:
    output.write(json.dumps(results, ensure_ascii=False, indent=4))