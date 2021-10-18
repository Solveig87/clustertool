import json
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import spacy
nlp = spacy.load('fr_core_news_sm')
import re

def pretrait(texte):

    """Supprime stopwords, ponctuation et mot de moins de 3 lettres d'un texte"""
    
    texte = texte.lower()
    texte = re.sub("marie-claire", "", texte)
    texte = re.sub(r"[-\']", " ", texte)
    texte = re.sub(r"\s+", " ", texte)
    
    return " ".join([token.text for token in nlp(texte) if len(token.text) > 2 and token.lemma_ not in ("faire", "très", "avoir") and not token.is_stop and not token.is_digit and not token.is_punct and not token.is_space])

def create_wordclouds(corpus, articleids):
    """Création du nuage de mots d'un cluster"""
    
    with open("data/" + corpus) as file:
        articles = json.load(file)
    
    cluster = pretrait(" ".join([" ".join([articles[articleid]['titre'], articles[articleid]['texte']]).strip() for articleid in articleids.split("+")]))
    vectorizer = TfidfVectorizer()
    count_data = vectorizer.fit_transform([cluster]).toarray()
    words = vectorizer.get_feature_names()
    
    cluster_words = {words[i]:count_data[0][i] for i in range(len(words))}
    wordcloud = WordCloud(collocations=True)
    wordcloud.generate_from_frequencies(cluster_words)

    plt.imshow(wordcloud, interpolation='bilInear')
    plt.axis('off')
    plt.savefig("frontend/static/img/nuage.png")

def print_article(corpus, articleid, words):

    with open("data/"+corpus) as file:
        articles = json.load(file)

    for word in [re.sub("-", " ", word) for word in words.split("_")]:
        if corpus == "ocr_corpus.json":
            articles[articleid]['text_withtags'] = re.sub(rf"(\b{word}\b)", r'<strong class="words">\1</strong>', articles[articleid]['texte'])
        else:
            articles[articleid]['text_withtags'] = re.sub(rf"(\b{word}\b)", r'<strong class="words">\1</strong>', articles[articleid]['text_withtags'])
    return articles[articleid]