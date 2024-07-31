from .Scraper import Scraper
from .Analisys import Analysis
import logging

class Intermediate:
    tosearch:str

    def __init__(self, tosearch:str):
        self.tosearch = tosearch
        self.scraper = Scraper
        self.analisys = Analysis
        
    def getData(self):
        try:
            isError = 0

            data = self.scraper.GetData(self.tosearch)

            for i in data:
                if data[i] == []:
                    isError += 1
            
            if isError < 4:
                return data
        except:
            logging.exception('error')
    def getSimilarity(self):
        try:
            data = self.getData()

            if data == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'similarity'}

            similar = self.analisys.Similarity(self.tosearch, data)
            if len(similar) != 0:
                return similar
        except:
            logging.exception('error')
    def getSentiment(self):
        try:
            corpus = self.getCorpus()
            
            if corpus == []:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'sentiment'}

            sentiment = self.analisys.SentimentAnalisys(corpus)

            if sentiment != []:
                return sentiment
        except:
            logging.exception('error')
    def getCorpus(self):
        try:
            similarity = self.getSimilarity()

            if similarity == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'corpus'}

            corpus = self.scraper.GetCorpus(similarity)

            if corpus != []:
                return corpus
        except:
            logging.exception('error')
    def getDate(self):
        try:
            similarity = self.getSimilarity()

            if similarity == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'getDate'}

            date = self.scraper.Getdate(similarity)

            if date != []:
                return date
        except:
            logging.exception('error')