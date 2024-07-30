from flask import Flask, request
from .teste import Intermediate
import logging

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return {'msg':'Welcome 😁', 'origin':'python'},200

@app.route('/v1/scraping/similarity', methods=['POST'])
def v1_similar():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    try:
        get_similar = Intermediate(request.json['userQuery']).similarity()
        if len(get_similar) == 0:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
        return get_similar,200
    except:
        logging.exception('error')