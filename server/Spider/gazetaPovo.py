import requests
from bs4 import BeautifulSoup
from ..items import Noticias

class SpiderGazeta:
    def __init__(self, source):
        self.source = source['gazeta']

    def fetch(self, query:str):
        req = requests.get(self.source['link_busca'] + query.replace(" ", "+"))
        req.status_code
        return BeautifulSoup(req.content, 'html.parser')

    def parse_titulo(self, noticia):
        return [titulo.get_text().strip() for titulo in noticia.find_all(class_=f"{self.source['titulo']}")]

    def parse_subtitulo(self, noticia):
        return [subtitulo.get_text().strip() for subtitulo in noticia.find_all(class_=f"{self.source['subtitulo']}")]

    def parse_dataPublicacao(self, noticia):
        return [data.get_text() for data in noticia.find_all(class_=f"{self.source['dataPublicacao']}")]

    def parse_link(self, noticia):
        return [link.get('href') for link in noticia.find_all(class_=f"{self.source['link']}")]
    
    def request_content(self, query:str):
        soup = self.fetch(query)
        noticias = soup.find_all(class_=self.source['divPai'])

        temp = []
        for noticia in noticias:
            titulo = self.parse_titulo(noticia=noticia)
            subtitulo = self.parse_subtitulo(noticia=noticia)
            dataPubli = self.parse_dataPublicacao(noticia=noticia)
            link = self.parse_link(noticia=noticia)

            temp.append(
                Noticias(
                    titulo=titulo,
                    subtitulo=subtitulo,
                    data_publicacao=dataPubli,
                    link=link
                )
            )
        return temp