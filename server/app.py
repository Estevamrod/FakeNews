from flask import Flask, request
from .Classes.intermediate import Intermediate
import logging

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return {'msg':'Welcome 😁', 'origin':'python'},200

@app.route('/v1/data', methods=['POST'])
def getdata():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    
    try:
        data = Intermediate(request.json['userQuery']).getData()

        if data != {}:
            return data,200
        else: 
            return {'msg':'Ocorreu um erro. Por favor tente novamente mais tarde!'}
    except:
        logging.exception('error')

@app.route('/v1/similarity', methods=['POST'])
def v1_similar():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    try:
        get_similar = Intermediate(request.json['userQuery']).getSimilarity()
        if get_similar != {}:
            return get_similar,200
        else:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
    except:
        logging.exception('error')

@app.route('/v1/sentiment', methods=['POST'])
def sentiment():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    try:
        sentiment = Intermediate(request.json['userQuery']).getSentiment()
        
        if sentiment == []:
            return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
        return sentiment, 200
    except:
        logging.exception('error')

@app.route('/v1/corpus', methods=['POST'])
def corpus():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    try:
        corpus = Intermediate(request.json['userQuery']).getCorpus()

        if corpus == []:
            return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
        return corpus, 200
    except:
        logging.exception('error')

@app.route('/v1/date', methods=['POST'])
def date():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    try:
        date = Intermediate(request.json['userQuery']).getDate()

        if date == []:
            return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
        return date, 200
    except:
        logging.exception('error')