from gevent import monkey
monkey.patch_all()
from flask import Flask, request
from .Classes.intermediate import Intermediate
import logging
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/v1/*": {"origins":"*"}})

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
        data = Intermediate(request.json['userQuery']).getData()
        if data == {}:
            return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'similarity'}

        get_similar = Intermediate(request.json['userQuery']).getSimilarity(data)
        if get_similar != {}:
            return get_similar,200
        else:
            return {'msg':'Ocorreu um erro ao finalizar a tarefa. Por favor tente novamente!'},201
    except:
        logging.exception('error')
@app.route('/v1/news', methods=['POST'])
def v1_newstosearch():
    try:
        if request.json['userQuery'] == "":
            return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
        ##Objetivos --> Executar similaridade, sentimento (precisa de corpus) e date
        intermediate = Intermediate(request.json['userQuery'])

        getdata = intermediate.getData()
        getsimilar = intermediate.getSimilarity(getdata)
        getcorpus = intermediate.getCorpus(getsimilar)
        getsentiment = intermediate.getSentiment(getcorpus)
        getdate = intermediate.getDate(getsimilar)

        if getdata != {} or getsimilar != {} or getdate != {}:
            return {'similarity':getsimilar, 'sentiment': getsentiment, 'date':getdate},200
    except:
        logging.exception('error')

@app.route('/v1/sentiment', methods=['POST'])
def sentiment():
    if request.json['userQuery'] == "":
        return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
    try:
        data = Intermediate(request.json['userQuery']).getCorpus()

        sentiment = Intermediate(request.json['userQuery']).getSentiment(data)
        
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
        data = Intermediate(request.json['userQuery']).getData()
        if data == {}:
            return {'msg':'Não foi possível finalizar a execução, por favor tente novamente!'},201
        
        corpus = Intermediate(request.json['userQuery']).getCorpus(data)

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')