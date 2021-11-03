import json
import argparse
from collections import Counter
import pandas as pd
import altair as alt

parser = argparse.ArgumentParser(description = "fichier")
parser.add_argument("-v", "--verbose", help = "verbose mode", action = "store_true")
parser.add_argument("corpus", help = "path of json file")
args = parser.parse_args()

def get_streamchart(data, ngram_size):

    keywords_cnt =  Counter()
    for annee, clusters in data['results'].items():
        for cluster in clusters:
            for keyword in cluster[ngram_size]:
                keywords_cnt[keyword] += 1
                
    selected_kw = [word for word, cnt in keywords_cnt.most_common(20)]

    visu_list = []
    for annee, clusters in data['results'].items():
        for kw in selected_kw:
            dic = {}
            dic['word'] = kw
            dic['year'] = annee.split("-")[0]
            cnt = 0
            for cluster in clusters:
                if kw in cluster[ngram_size]:
                    cnt += len(cluster['articles'])
            dic['count'] = cnt / sum([len(cluster['articles']) for cluster in data['results'][annee]])
            visu_list.append(dic)

    dataf = pd.DataFrame(visu_list)
    #print(dataf)

    chart = alt.Chart(dataf).mark_area().encode(
        alt.X('year:T',
            axis=alt.Axis(format='%Y', domain=False, tickSize=0)
        ),
        alt.Y('count:Q', stack='center', axis=None),
        alt.Color('word:N',
            scale=alt.Scale(scheme='category20b')
        )
    ).interactive()

    pathname = "results/streamcharts/" + args.corpus.split("/")[-1].split(".")[0] + '_' + ngram_size[0] + '_chart.html'
    chart.save(pathname)

with open(args.corpus) as f:
    data = json.load(f)
for i in range(1,4):
    ngram_size = str(i) + "-grams"
    print("streamgraph : ", ngram_size)
    get_streamchart(data, ngram_size)