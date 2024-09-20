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
            else:
                return {}
        except:
            logging.exception('error')
    def getSimilarity(self, data:dict[str, list] | tuple[dict[str, str]]):
        try:
            if data == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'similarity'}

            similar = self.analisys.Similarity(self.tosearch, data)
            if len(similar) != 0:
                return similar
            else:
                return {}
        except:
            logging.exception('error')
    def getSentiment(self, data:dict[str, list] | tuple[dict[str, str]]):
        try:
            
            if data == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'sentiment'}

            sentiment = self.analisys.SentimentAnalisys(data)

            if sentiment != []:
                return sentiment
        except:
            logging.exception('error')
    def getCorpus(self, data:dict[str, list] | tuple[dict[str, str]]):
        try:
            if data == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'corpus'}

            corpus = self.scraper.GetCorpus(data)

            if corpus != []:
                return corpus
            else:
                return {}
        except:
            logging.exception('error')
    def getDate(self, data:dict[str, list] | tuple[dict[str, str]]):
        try:
            if data == {}:
                return {'msg':'Ocorreu um erro ao tentar finalizar a tarefa. Por favor tente novamente!', 'func':'getDate'}

            date = self.scraper.Getdate(data)

            if date != []:
                return date
        except:
            logging.exception('error')