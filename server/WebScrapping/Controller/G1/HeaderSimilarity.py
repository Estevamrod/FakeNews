from bs4 import BeautifulSoup
import requests
import spacy

def HeaderSimilarity(Newsu):
    i = 0
    Headers = {}
    Links = {}
    Articles = {}
    Similaridade = {}

    if Newsu != "":
        try: 
            data = requests.get('https://g1.globo.com/busca/?', params={'q': Newsu.replace(" ",'+'), 'order':'relevant'})
            print(f"status code: {data.status_code}")
            htmlContent = data.text

            soup = BeautifulSoup(htmlContent, 'html.parser')
            for news in soup.find_all(class_='widget--info__title product-color'):
                Headers[i] = {
                    'Headers': news.get_text().strip()
                }
                i += 1
            
            i = 0
            for links in soup.find_all(class_= 'widget--info__text-container'):
                PATH = links.find('a').get('href')
                Links[i] = {
                    'Links': PATH
                }
                i += 1
            
            for j in Headers:
                Articles[j] = {
                    'H1': Headers[j]['Headers'],
                    'A': Links[j]['Links']
                }
            
            nlp = spacy.load('pt_core_news_lg')
            i = 0
            for h1 in Articles.values():
                s1 = nlp(Newsu)
                s2 = nlp(h1['H1'])

                similar = round(s1.similarity(s2)*100, 2)
                Similaridade[i] = {
                    'Accuracy': f"{similar}%",
                    'Noticia': h1['H1'],
                    'Userquery': Newsu,
                    'Link': h1['A']
                }
                print(f"A similaridade e de: {s1.similarity(s2)*100:.2f}%")
                i += 1
            print(Similaridade.get(max(Similaridade, key=lambda k:Similaridade[k]['Accuracy'])))
        except Exception as e:
            print(e)
            return e
    return Similaridade[max(Similaridade, key=lambda k :Similaridade[k]['Accuracy'])]