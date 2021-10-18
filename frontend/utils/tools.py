import json
import re



def print_article(corpus, articleid, words):

    with open("data/"+corpus) as file:
        articles = json.load(file)

    for word in [re.sub("-", " ", word) for word in words.split("_")]:
        if corpus == "ocr_corpus.json":
            articles[articleid]['text_withtags'] = re.sub(rf"(\b{word}\b)", r'<strong class="words">\1</strong>', articles[articleid]['texte'])
        else:
            articles[articleid]['text_withtags'] = re.sub(rf"(\b{word}\b)", r'<strong class="words">\1</strong>', articles[articleid]['text_withtags'])
    return articles[articleid]