from flask import Response, render_template
from flask_restful import Resource

class Index(Resource):
	"""Classe Index"""

	def get(self):
		"""Méthode GET, affiche la page d'accueil"""

		index_rend = render_template("index.html")
		resp = Response(index_rend, status = 200, content_type = "text/html")
		return resp
