# Clustertool

## Présentation

Ce programme permet de visualiser les résultats du clustering (algorithme de type *Affinity Propagation*) des documents d'un corpus, année par année. Chaque cluster est présenté avec ses thématiques associées (topic modeling effectué avec un algorithme de type *LDA*), la liste des documents qui lui sont affectés et un nuage de mots. L'ensemble des résultats peut être visualisé grâce à des graphiques de type *Motionchart* et *Streamchart*.

## Utilisation

Pour tester sur d'autres données que celles fournies ici, voir le Readme du répertoire **generate_data**.

Se placer à la racine du projet et installer les *requirements* :

`pip install -r requirements.txt`

Puis lancer l'application :

`python run.py`

Copier ensuite l'url indiquée dans un navigateur.
