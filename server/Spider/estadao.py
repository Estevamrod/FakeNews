import requests
from bs4 import BeautifulSoup
from ..items import Noticias

class SpiderEstadao:
    def __init__(self, source):
        self.source = source['news_google']

    def fetch(self, query:str):
        req = requests.get(self.source['link_busca'] + query + " site:estadao.com.br when:1y&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
        req.status_code
        return BeautifulSoup(req.text, 'html.parser')
    
    def parse_titulo(self, noticia):
        for titulo in noticia.find_all(class_=f"{self.source['titulo']}"):
            return titulo.get_text()

    def parse_link(self, noticia):
        for link in noticia.find_all(class_=f"{self.source['link']}"):
            return link.get('href')

    def parse_dataPubli(self, noticia):
        return [data.get_text().strip() for data in noticia.find_all(class_=f"{self.source['dataPublicacao']}")]

    def request_content(self, query:str):
        soup = self.fetch(query=query)
        noticias = soup.find_all(class_=f"{self.source['divPai']}")

        temp_resultado = []
        for noticia in noticias:
            titulo = self.parse_titulo(noticia=noticia)
            link = self.parse_link(noticia=noticia)
            dataPublicacao = self.parse_dataPubli(noticia=noticia)

            temp_resultado.append(
                Noticias(
                    titulo=titulo,
                    subtitulo=None,
                    link=link,
                    data_publicacao=dataPublicacao,
                    fonte="estadao"
                )
            )
            
            return temp_resultado