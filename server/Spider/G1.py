import json
import requests
from bs4 import BeautifulSoup
from ..items import Noticias


class SpiderG1:
   def __init__(self, source):
      self.source = source['news_google']

   def fetch(self, querycontent:str):
      req = requests.get(self.source['link_busca'] + querycontent + " site:g1.globo.com when:1y&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
      req.status_code
      return BeautifulSoup(req.content, 'html.parser')

   def parse_titulo(self, noticia):
      for titulo in noticia.find(class_=f"{self.source['titulo']}"):
         return titulo.get_text()

   def parse_link(self, noticia):
      return [link.get('href') for link in noticia.find_all(class_=self.source['link'])]

   def parse_dataPubli(self, noticia):
      return [data.get_text() for data in noticia.find_all(class_=self.source['dataPublicacao'])]

   def request_content(self, query:str):
      soup = self.fetch(query)
      noticias = soup.find_all(class_=self.source['divPai'])

      Resultado = []
      for noticia in noticias:
         titulo = self.parse_titulo(noticia=noticia)
         link = self.parse_link(noticia=noticia)
         dataPublicacao = self.parse_dataPubli(noticia=noticia)

         Resultado.append(
            Noticias(
               titulo=titulo,
               subtitulo=None,
               link=link, 
               data_publicacao=dataPublicacao,
               fonte="g1"
            )
         )
      return Resultado