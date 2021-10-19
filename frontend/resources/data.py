# coding: utf-8

from flask import json, request, Response, render_template, Flask
from flask_restful import Resource
import requests

from ..utils import *

class Corpus(Resource):
    """Classe de Consultation d'un article"""

    def get(self):
        """Méthode GET, affiche la présentation des corpus"""

        corpus_rend = render_template("corpus.html")

        resp = Response(corpus_rend, status = 200, content_type = "text/html")
        return resp

class Statistiques(Resource):
    """Classe de Consultation d'un article"""

    def get(self, corpus):
        """Méthode GET, affiche les statistiques d'un corpus"""

        path_data = "data/stats_" + corpus + ".json"
        with open(path_data) as file:
            results = json.load(file)
        results['corpus'] = corpus

        stats_rend = render_template("stats.html", results = results)

        resp = Response(stats_rend, status = 200, content_type = "text/html")
        return resp


class Clustering(Resource):
    """Classe de clustering de données"""

    def get(self):
        """Méthode GET, affiche le formulaire pour le choix des paramètres de clustering.
        Si un formulaire a été soumis, affiche les résultats."""

        filtres = dict(request.args)
            
        # cas où aucune recherche n'a été effectuée
        if not filtres :
            clustering_rend = render_template("clustering.html")
            resp = Response(clustering_rend, status = 200, content_type = "text/html")
            return resp

        # cas où une recherche a été effectuée
        else :
            path_data = "data/" + filtres.get('corpus') + "_" + filtres.get('time_window') + ".json"
            with open(path_data) as file:
                results = json.load(file)
            results['path'] = path_data.split('/')[-1].split(".")[0]
            clustering_rend = render_template("clustering.html", search = True, results = results)
            resp = Response(clustering_rend, status = 200, content_type = "text/html")
            return resp


class Article(Resource):
    """Classe de Consultation d'un article"""

    def get(self, corpus, articleid, words):
        """Méthode GET, affiche le contenu d'un article du corpus"""

        api_response = requests.get(backend_api + "/"+corpus+"/"+articleid+"/"+words, headers=make_headers(), verify=False)

        article = print_article(corpus, articleid, words)

        article_rend = render_template("article.html", article = article)

        resp = Response(article_rend, status = 200, content_type = "text/html")
        return resp

from flask import send_file

class Motionchart(Resource):
    """Classe de visualisation en motionchart"""

    def get(self, lda_result):
        """Méthode GET, affiche les résultats dans un graphique en mouvement"""

        path_file = "motioncharts/" + lda_result + ".html"
        article_rend = render_template(path_file)

        resp = Response(article_rend, status = 200, content_type = "text/html")
        return resp
    
class StreamGraph(Resource):
    """Classe de visualisation en motionchart"""

    def get(self, lda_result):
        """Méthode GET, affiche les résultats dans un graphique en mouvement"""

        path_file = "streamcharts/" + lda_result + "_chart.html"
        article_rend = render_template(path_file)

        resp = Response(article_rend, status = 200, content_type = "text/html")
        return resp

class Wordcloud(Resource):
    """Classe de création d'un nuage de mots"""

    def get(Resource, corpus, annee, cluster):

        filename = "static/img/nuages/" + corpus + "_" + annee + "_" + cluster + ".png"

        return send_file(filename, mimetype='image/gif')
