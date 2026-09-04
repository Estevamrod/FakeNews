import requests
from bs4 import BeautifulSoup
from ..items import Noticias

class SpiderGazeta:
    def __init__(self, source):
        self.source = source
        self.backupSource = False

    def fetch(self, query:str):
        try:
            req = requests.get(self.source['gazeta']['link_busca'] + query.replace(" ", "+"))
        except requests.exceptions.ProxyError:
            req = requests.get(self.source['news_google']['link_busca'] + query + " site:gazetadopovo.com.br when:1y&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
            self.backupSource = True
        req.status_code
        return BeautifulSoup(req.content, 'html.parser')

    def parse_titulo(self, noticia):
        if not self.backupSource:
            for titulo in noticia.find(class_=f"{self.source['gazeta']['titulo']}"):
                return titulo.get_text().strip()
        else:
            for titulo in noticia.find(class_=f"{self.source['news_google']['titulo']}"):
                return titulo.get('aria-label').split(' - ')[0]

    def parse_subtitulo(self, noticia):
        if self.backupSource:
            return None

        for subtitulo in noticia.find(class_=f"{self.source['gazeta']['subtitulo']}"):
            return subtitulo.get_text().strip()

    def parse_dataPublicacao(self, noticia):
        if not self.backupSource:
            for data in noticia.find(class_=f"{self.source['gazeta']['dataPublicacao']}"):
                return data.get_text()
        else: 
            for data in noticia.find(class_=f"{self.source['news_google']['dataPublicacao']}"):
                return data.get_text()

    def parse_link(self, noticia):
        if not self.backupSource:
            for link in noticia.find(class_=f"{self.source['gazeta']['link']}"):
                return link.get('href')
        else:
            for link in noticia.find(class_=f"{self.source['news_google']['link']}"):
                return link.get('href')
    
    def request_content(self, query:str):
        soup = self.fetch(query)
        noticias_card = soup.find_all(class_=self.source['gazeta']['divPai']) 

        if not noticias_card:
            soup.find_all(class_=f"{self.source['news_google']['divPai']}")

        temp = []
        for noticia in noticias_card:
            titulo = self.parse_titulo(noticia=noticia)
            subtitulo = self.parse_subtitulo(noticia=noticia)
            dataPubli = self.parse_dataPublicacao(noticia=noticia)
            link = self.parse_link(noticia=noticia)

            temp.append(
                Noticias(
                    titulo=titulo,
                    subtitulo=subtitulo,
                    data_publicacao=dataPubli,
                    link=link,
                    fonte="gazeta"
                )
            )
        return temp