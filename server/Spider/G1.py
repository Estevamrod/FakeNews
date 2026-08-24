import requests
from bs4 import BeautifulSoup
from ..items import Noticias

import logging


class SpiderG1:
  def __init__(self, source):
    self.source = source['g1']

  def fetch(self, querycontent:str):
    req = requests.get(self.source['link_busca'] + querycontent + " site:g1.globo.com when:1y&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
    req.status_code
    return BeautifulSoup(req.content, 'html.parser')

  def parse_titulo(self, soup):
      
      return [titulo.get('aria-label').split(' - ')[0] for titulo in soup.find_all(class_=f"{self.source['titulo']}")]

  def parse_link(self, soup):
    return [f"https://news.google.com{link.get('href')}" for link in soup.find_all(class_=self.source['link'])]

  def append(self, soup):
      return Noticias(
      titulo=self.parse_titulo(soup),
      subtitulo="",
      link=self.parse_link(soup),
      fonte="G1"
    )

  def request_content(self, query:str):
    soup = self.fetch(query)
    print(self.parse_titulo(soup))
    data = self.append(soup)
    return data
