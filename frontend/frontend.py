# coding: utf-8
from flask import Flask
from flask_restful import Resource, Api
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
api = Api(app)

app.config.from_pyfile('config.py')

from .resources import *

api.add_resource(Index, "/", "/index")
api.add_resource(Clustering, "/clustering")
api.add_resource(Article, "/<corpus>/<articleid>/<words>")
api.add_resource(Wordcloud, "/nuage/<corpus>/<cluster>")
api.add_resource(Motionchart, "/motioncharts/<lda_result>")
api.add_resource(StreamGraph, "/streamcharts/<lda_result>")
api.add_resource(Corpus, "/corpus")
api.add_resource(Statistiques, "/stats/<corpus>")

if __name__ == '__main__':
	app.run(debug=True)
