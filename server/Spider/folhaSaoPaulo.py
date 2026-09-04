import requests
import json
from bs4 import BeautifulSoup
from ..items import Noticias

class SpiderFolha:
    def __init__(self, source):
        self.source = source
        self.backupSource = False

    def fetch(self, query:str):
        try:
            req = requests.get(self.source['folha']['link_busca'] + query.replace(" ", "+"))
        except requests.exceptions.ProxyError:
            req = requests.get(self.source['news_google']['link_busca'] + query + " site:folha.uol.com.br when:1y&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
            self.backupSource = True
        req.status_code
        req.encoding = "UTF-8"
        return BeautifulSoup(req.content, 'html.parser')
    
    def parse_titulo(self, noticia):
        if not self.backupSource:
            for titulo in noticia.find(class_=f"{self.source['folha']['titulo']}"):
                return titulo.get_text().strip()
        else:
            for titulo in noticia.find_all(class_=f"{self.source['news_google']['titulo']}"):
                return titulo.get('aria-label').split(' - ')[0]

    def parse_subtitulo(self, noticia):
        if self.backupSource:
            return None

        for subtitulo in noticia.find(class_=f"{self.source['folha']['subtitulo']}"):
            return subtitulo.get_text().strip()

    def parse_dataPubli(self, noticia):
        if not self.backupSource:
            for data in noticia.find_all(class_=f"{self.source['folha']['dataPublicacao']}"):
                return data.get('datetime')
        else:
            for data in noticia.find_all(class_=f"{self.source['news_google']['dataPublicacao']}"):
                return data.get_text()

    def parse_link(self, noticia):
        if not self.backupSource:
            return noticia.find_next().get('href')
        else:
            for link in noticia.find_all(class_=f"{self.source['news_google']['link']}"):
                return link.get('href')
    
    def request_content(self, query:str):
        soup = self.fetch(query=query)
        noticias_card = soup.find_all(class_=f"{self.source['folha']['divPai']}")

        if not noticias_card:
            noticias_card = soup.find_all(class_=f"{self.source['news_google']['divPai']}")

        tempResultado = []
        for noticia in noticias_card:
            titulo = self.parse_titulo(noticia=noticia)
            subtitulo = self.parse_subtitulo(noticia=noticia)
            dataPubli = self.parse_dataPubli(noticia=noticia)
            link = self.parse_link(noticia=noticia)

            tempResultado.append(
                Noticias(
                    titulo=titulo,
                    subtitulo=subtitulo,
                    data_publicacao=dataPubli,
                    link=link,
                    fonte="folha"
                )
            )
        return tempResultado