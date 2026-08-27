import requests
from bs4 import BeautifulSoup
from ..items import Noticias

class SpiderFolha:
    def __init__(self, source):
        self.source = source['folha']

    def fetch(self, query:str):
        req = requests.get(self.source['link_busca'] + query.replace(" ", "+"))
        req.status_code
        return BeautifulSoup(req.content, 'html.parser')
    
    def parse_titulo(self, noticia):
        return [titulo.get_text().strip() for titulo in noticia.find_all(class_=f"{self.source['titulo']}")]

    def parse_subtitulo(self, noticia):
        return [subtitulo.get_text().strip() for subtitulo in noticia.find_all(class_=f"{self.source['subtitulo']}")]

    def parse_dataPubli(self, noticia):
        return [data.get('datetime') for data in noticia.find_all(class_=f"{self.source['dataPublicacao']}")]

    def parse_link(self, noticia):
        linkCore = noticia.find_all(class_=f"{self.source['link']}")
        return [link.get('href') for link in linkCore.find('a')]
    
    def request_content(self, query:str):
        soup = self.fetch(query=query)
        noticias = soup.find_all(class_=f"{self.source['divPai']}")

        tempResultado = []
        for noticia in noticias:
            titulo = self.parse_titulo(noticia=noticia)
            subtitulo = self.parse_subtitulo(noticia=noticia)
            dataPubli = self.parse_dataPubli(noticia=noticia)
            link = self.parse_link(noticia=noticia)

            tempResultado.append(
                Noticias(
                    titulo=titulo,
                    subtitulo=subtitulo,
                    data_publicacao=dataPubli,
                    link=link
                )
            )
        return tempResultado