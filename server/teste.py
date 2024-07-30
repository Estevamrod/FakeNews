from .Classes.Scraper import Scraper
from .Classes.Analisys import Analysis

class Intermediate:
    tosearch:str
    
    def __init__(self, tosearch:str):
        self.tosearch = tosearch
        self.scraper = Scraper
        self.analisys = Analysis(self.tosearch)
        
    def data(self):
        return self.scraper.GetData(self.tosearch)
    def similarity(self):
        return self.analisys.Similarity()