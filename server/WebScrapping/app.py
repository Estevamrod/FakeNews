from flask import Flask, request
from Scraper import Scraper as sc
app = Flask(__name__)

@app.route('/scrapping', methods=['POST'])
def webscrapping():
    if request.json != {}:
        sentimentAnalisys = sc(request.json['userQuery']).SentimentAnalisys()
        # GetCorpus = sc(request.json['userQuery']).GetCorpus()
        # Similarity = sc(request.json['userQuery']).GetSimilarity()
        # GetData = sc(request.json['userQuery']).GetData()
        print(request.headers)
        # return {
        #     'Analise_de_Sentimento': sentimentAnalisys,
        #     'GetCorpus': GetCorpus,
        #     'Similarity': Similarity,
        #     'Getdata': GetData
        # }
        return sentimentAnalisys