from flask import Flask, request
from Scraper import Scraper as sc
import logging
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return {'msg':'Welcome 😁', 'origin':'python'},200


@app.route('/v1/scraping/getdata', methods=['POST'])
def v1_getdata():
    if request.json == {}:
        return {'msg':'Você precisa realizar uma requisição com o conteúdo no body da página'},201
    try:
        isError = 0
        get_data = sc(request.json['userQuery']).GetData()
        for i in get_data:
            if get_data[i] == []:
                isError += 1
        
        if isError < 4:
            return get_data,200
        else:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
    except Exception as e:
        return e, 201

@app.route('/v1/scraping/similarity', methods=['POST'])
def v1_similar():
    if request.json == {}:
        return {'msg':'Você precisa realizar uma requisição com o conteúdo no body da página'},201
    try:
        isError = 0
        get_similar = sc(request.json['userQuery']).GetSimilarity()
        for i in get_similar:
            if get_similar[i]['titulo_mais_similar'] == [] and get_similar[i]['subtitulo_mais_similar'] == []:
                isError += 1
        if isError < 4:
            return get_similar,200
        else :
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
    except Exception as e:
        return e, 201

@app.route('/v1/scraping/getcorpus', methods=["POST"])
def v1_corpus():
    if request.json == {}:
        return {'msg':'Você precisa realizar uma requisição com o conteúdo no body da página'},201
    try:
        get_corpus = sc(request.json['userQuery']).GetCorpus()
        if get_corpus == []:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
        return get_corpus,200
    except Exception as e:
        logging.exception('error')
        return e, 201
    
@app.route('/v1/scraping/sentiment', methods=['POST'])
def v1_sentiment():
    if request.json == {}:
        return {'msg':'Você precisa realizar uma requisição com o conteúdo no body da página'},201
    try:
        get_sentiment = sc(request.json['userQuery']).SentimentAnalisys()

        if get_sentiment == []:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
        
        return get_sentiment,200
    except Exception as e:
        return e, 201
    

@app.route('/v1/scraping/getdate', methods=['POST'])
def v1_date():
    if request.json == {}:
        return {'msg':'Você precisa realizar uma requisição com o conteúdo no body da página'},201
    try:
        get_date = sc(request.json['userQuery']).get_date()
        if get_date == []:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
        return get_date,200
    except Exception as e:
        return e, 201
