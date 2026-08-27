import requests
from bs4 import BeautifulSoup
from ..items import Noticias

class SpiderEstadao:
    def __init__(self, source):
        self.source