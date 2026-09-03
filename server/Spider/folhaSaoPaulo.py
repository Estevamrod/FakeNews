import requests
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
        return BeautifulSoup(req.content, 'html.parser')
    
    def parse_titulo(self, noticia):
        return [titulo.get_text().strip() for titulo in noticia.find_all(class_=f"{self.source['folha']['titulo']}")] if not self.backupSource else [titulo.get('aria-label').split(' - ')[0] for titulo in noticia.find_all(class_=f"{self.source['news_google']['titulo']}")]

    def parse_subtitulo(self, noticia):
        return [subtitulo.get_text().strip() for subtitulo in noticia.find_all(class_=f"{self.source['folha']['subtitulo']}")] if not self.backupSource else None

    def parse_dataPubli(self, noticia):
        return [data.get('datetime') for data in noticia.find_all(class_=f"{self.source['folha']['dataPublicacao']}")] if not self.backupSource else [data.get_text() for data in noticia.find_all(class_=f"{self.source['news_google']['dataPublicacao']}")]

    def parse_link(self, noticia):
        if not self.backupSource:
            linkCore = noticia.find_all(class_=f"{self.source['folha']['link']}")
            return [link.get('href') for link in linkCore.find('a')]
        else:
            return [link.get('href') for link in noticia.find_all(class_=f"{self.source['news_google']['link']}")]
    
    def request_content(self, query:str):
        soup = self.fetch(query=query)
        noticias = soup.find_all(class_=f"{self.source['folha']['divPai']}")

        if not noticias:
            noticias = soup.find_all(class_=f"{self.source['news_google']['divPai']}")

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
                    link=link,
                    fonte="Folha"
                )
            )
        return tempResultado