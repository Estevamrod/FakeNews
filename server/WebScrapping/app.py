from Controller.Scraper import Scraper as sc
from flask import Flask, request
from Controller.G1 import HeaderSimilarity as Hs
from Controller.G1 import Articledata as Ad
app = Flask(__name__)

@app.route('/scrapping', methods=['POST'])
def webscrapping():
    if request.json != {}:
        data = sc(request.json['userQuery']).GetSimilarity()
        # data = Hs.HeaderSimilarity(request.json['userQuery'])
        # date = Ad.ArticleInfo(data['Link'])
        # print(date.GetDate()) 
        print(request.headers)
        return data