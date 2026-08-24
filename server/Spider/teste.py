import requests
from bs4 import BeautifulSoup


req = requests.get("https://news.google.com/search?q=" + "Vacina da dengue do instituto butantan" + " site:g1.globo.com when:1y&hl=pt-BR&gl=BR&ceid=BR%3Apt-419")
print(req.status_code)
soup = BeautifulSoup(req.text, 'html.parser')

for titulo in soup.find_all(class_='JtKRv'):
  print(f"content: {titulo.get_text().strip()}, link: https://news.google.com{titulo.get('href')}")