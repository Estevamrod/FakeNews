from flask import Flask, request
from Controller.G1 import HeaderSimilarity as Hs

app = Flask(__name__)

@app.route('/scrapping', methods=['POST'])
def webscrapping():
    if request.json != {}:
        data = Hs.HeaderSimilarity(request.json['userQuery'])
        print(request.headers)
        return data