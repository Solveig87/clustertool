from motionchart.motionchart import MotionChart, MotionChartDemo
import webbrowser
import json
import argparse
from collections import Counter
import pandas as pd

parser = argparse.ArgumentParser(description = "fichier")
parser.add_argument("-v", "--verbose", help = "verbose mode", action = "store_true")
parser.add_argument("corpus", help = "path of json file")
args = parser.parse_args()

"""Ouverture du fichier json"""

with open(args.corpus) as f:
    data = json.load(f)

"""Sélection des 20 ngrams les plus souvent choisis par LDA pour représenter un cluster"""

keywords_cnt =  Counter()
for annee, clusters in data['results'].items():
    for cluster in clusters:
        ngrams = cluster['1-grams'] + cluster['2-grams'] + cluster['3-grams']
        for keyword in ngrams:
            keywords_cnt[keyword] += 1
            
selected_kw = [word for word, cnt in keywords_cnt.most_common(20)]

"""Création du dataframe"""

visu_list = []
for annee, clusters in data['results'].items():
    for kw in selected_kw:
        dic = {}
        dic['word'] = kw
        dic['year'] = annee
        dic['total_clusters'] = keywords_cnt[kw]
        dic['ngram_size'] = len(kw.split())
        cnt_art = 0
        cnt_clusters = 0
        for cluster in clusters:
            ngrams = cluster['1-grams'] + cluster['2-grams'] + cluster['3-grams']
            if kw in ngrams:
                cnt_clusters += 1
                cnt_art += len(cluster['articles'])
        dic['cnt_art'] = cnt_art / sum([len(cluster['articles']) for cluster in data['results'][annee]])
        dic['cnt_clusters'] = cnt_clusters / len(clusters)
        visu_list.append(dic)

dataf = pd.DataFrame(visu_list)

"""Création de la visualisation diachronique dynamique"""

mChart = MotionChart(df = dataf, key = 'year', x = 'total_clusters', y = 'cnt_clusters', size = 'cnt_art', color = 'ngram_size', category = 'word')
mChart.to_browser()