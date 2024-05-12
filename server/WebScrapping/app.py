from flask import Flask, request
from Scraper import Scraper as sc
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return {'msg':'There? Its OK!', 'origin':'python'},200


@app.route('/scrapping', methods=['POST'])
def webscrapping():
    if request.json != {}:
        try:
            # sentimentAnalisys = sc(request.json['userQuery']).SentimentAnalisys()
            # GetCorpus = sc(request.json['userQuery']).GetCorpus()
            # Similarity = sc(request.json['userQuery']).GetSimilarity()
            # GetData = sc(request.json['userQuery']).GetData()
            get_date = sc(request.json['userQuery']).get_date()
            print(request.headers)
            # return {
            #     'Analise_de_Sentimento': sentimentAnalisys,
            #     'GetCorpus': GetCorpus,
            #     'Similarity': Similarity,
            #     'Getdata': GetData
            # }
            return get_date
        except Exception as e:
            print('app')
            print(e)
            return e