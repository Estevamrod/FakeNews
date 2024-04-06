import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import grequests
from bs4 import BeautifulSoup
import requests
import spacy
import json

class Scraper:
    def __init__(self, newstoSearch):
        self.newstoSearch = newstoSearch

    def GetData(self):  ## Aqui a gente vai utilizar para "pegar" os titulos, manchetes e os links de cada noticia
        if self.newstoSearch == "":
            return {'msg': 'Você está fazendo uma requisição, mas não cumprindo com todos os requisitos!', 'finished': False, 'error': True}, 200
        searchEngineStandart = [ 
            'https://g1.globo.com/busca/?order=relevant&', 
            #G1
            'https://search.folha.uol.com.br/?site=todos&',
            # Folha de São Paulo
            'https://www.gazetadopovo.com.br/busca/?', ## Utiliza q
            # Gazeta do Povo
            'https://busca.estadao.com.br/?',
            # Estadao
            
        ]
        # searchEngineGoogle = [
        #     'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=pt-PT&source=gcsc&gss=.com&cselibv=8435450f13508ca1&cx=004590593083191455447%3A5j_p3qfagic&safe=off&cse_tok=AB-tC_7ewW0pO9BEfIR_jEBFa923%3A1709937160692&sort=&exp=cc%2Cdtsq-3&fexp=72497452&callback=google.search.cse.api5181&',
        #     # UOL
        #     'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=pt-BR&source=gcsc&gss=.br&cselibv=8435450f13508ca1&cx=33c20c29942ff412b&safe=off&cse_tok=AB-tC_6O_nEFvMPcLyCF3I43OvcT%3A1709937247606&lr=&cr=&gl=&filter=0&sort=&as_oq=&as_sitesearch=*.uol.com.br%2F*&exp=cc&fexp=72522726%2C72523582%2C72497452&callback=google.search.cse.api14043&',
        #     # Metropoles
        # ]
        data = []
        try:
            ## FILTRO => resultado = list(filter(lambda x: x['site'] == 'estado', data))
            req = [grequests.get(str(url) + 'q=' + self.newstoSearch.replace(" ", "+")) for url in searchEngineStandart]
            responses = grequests.map(req, size=2)
            for response in responses:
                print(f"status_code:{response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')
                ##inicio g1 
                for gTitulo in soup.find_all(class_='widget--info__title product-color'):
                    data.append({'site_url':searchEngineStandart[0], 'site_name':'G1', 'dados':{'titulo':gTitulo.get_text().strip()}})
                g1 = list(filter(lambda x: x['site_name'] == 'G1', data))
                i = 0
                for gSubtitulo in soup.find_all(class_='widget--info__description'):
                    if i < len(g1):
                        g1[i]['dados']['subtitulo'] = gSubtitulo.get_text().strip()
                        i+= 1
                i = 0
                for gLink in soup.find_all(class_='widget--info__text-container'):
                    if i < len(g1):
                        g1[i]['dados']['Link'] = gLink.find('a').get('href')
                        i+= 1
                ##fim g1
                ##inicio folha
                for fTitulo in soup.find_all(class_='c-headline__title'):
                    data.append({'site_url':searchEngineStandart[1], 'site_name':'Folha_de_sao_paulo', 'dados': {'titulo':fTitulo.get_text().strip()}})
                folha = list(filter(lambda x: x['site_name'] == 'Folha_de_sao_paulo', data))
                i = 0
                for fSubtitulo in soup.find_all(class_='c-headline__standfirst'):
                    if fSubtitulo.get_text().strip() != 'O jornal Folha de S.Paulo é publicado pela Empresa Folha da Manhã S.A. CNPJ: 60.579.703/0001-48' and i < len(folha):
                        folha[i]['dados']['subtitulo'] = fSubtitulo.get_text().strip()
                        i += 1
                i = 0
                for fLink in soup.find_all(class_='c-headline__content'):
                    if i < len(folha):
                        folha[i]['dados']['Link'] = fLink.find('a').get('href')
                        i += 1
                ## Fim Folha
                ## Gazeta do Povo
                for gpTitulo in soup.find_all(class_='post-title'):
                    data.append({'site_url': searchEngineStandart[2], 'site_name':'Gazeta_do_povo', 'dados':{'titulo': gpTitulo.get_text().strip()}})
                gp = list(filter(lambda x: x['site_name'] == 'Gazeta_do_povo', data))
                i = 0
                for gpSubtitulo in soup.find_all(class_='post-summary'):
                    if i < len(gp):
                        gp[i]['dados']['subtitulo'] = gpSubtitulo.get_text().strip()
                        i += 1
                i = 0
                for gpLink in soup.find_all(class_='post-url'):
                    if i < len(gp):
                        gp[i]['dados']['Link'] = gpLink.get('href')
                        i += 1
                ## Fim Gazeta
                ## Estadao
                for estadoTitulo in soup.find_all(class_='link-title'):
                    data.append({'site_url':searchEngineStandart[3], 'site_name':'Estadao', 'dados':{'titulo': estadoTitulo.find('h3').get_text().strip(), 'Link': estadoTitulo.get('href')}})
                
                estadao = list(filter(lambda x: x['site_name'] == 'Estadao', data))
                i = 0
                for estadoSubtitulo in soup.find_all(class_='link-title'):
                    for item in estadoSubtitulo.find_all('p'):
                        if i < len(estadao):
                            estadao[i]['dados']['subtitulo'] = "Nao possui subtitulo" if item.get_text().strip() == '' else item.get_text().strip()
                            i += 1
            
            return {
                'Folha_de_sao_paulo': folha,
                'G1': g1,
                'Estadao': estadao,
                'Gazeta_do_povo': gp
            }
        except Exception as e:
            print(e)

    def GetSimilarity(self): ## Após "pegar" as informações de um conjunto de notícias, precisamos agora análisar cada titulo e subtitulo para ver qual notícia é mais adequada com o que o usuário pesquisou
        Similaridade = []

        try:
            response = self.GetData()
            ## Inicio G1
            nlp = spacy.load('pt_core_news_lg') ## Para carregar o pacote que usaremos para analisar os titulos e as manchetes
            s1 = nlp(self.newstoSearch) ## Cria um objeto com as informações estruturais gramaticais e semânticas do texto

            for gTitulo in response['G1']:
                s2 = nlp(gTitulo['dados']['titulo'])
                Similaridade.append({'Similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': gTitulo['dados']['titulo'], 'Link_Noticia': gTitulo['dados']['Link']}, 'site_name':'G1'})

            g1Similar = list(filter(lambda x: x['site_name'] == 'G1', Similaridade))
            i = 0
            for gSubtitulo in response['G1']:
                s2 = nlp(gSubtitulo['dados']['subtitulo'])

                g1Similar[i]['Similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                g1Similar[i]['Similaridade']['subtitulo_original'] = gSubtitulo['dados']['subtitulo']
                i += 1
            ## fim g1
            ## Inicio Folha
            for fTitulo in response['Folha_de_sao_paulo']:
                s2 = nlp(fTitulo['dados']['titulo'])
                Similaridade.append({'Similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': fTitulo['dados']['titulo'], 'Link_Noticia': fTitulo['dados']['Link']}, 'site_name':'Folha_De_Sao_paulo'})

            folhaSimiliar = list(filter(lambda x: x['site_name'] == 'Folha_De_Sao_paulo', Similaridade))
            i=0
            for fSubtitulo in response['Folha_de_sao_paulo']:
                s2 = nlp(fSubtitulo['dados']['subtitulo'])

                folhaSimiliar[i]['Similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                folhaSimiliar[i]['Similaridade']['subtitulo_original'] = fSubtitulo['dados']['subtitulo']
                i += 1

            ## Fim Folha
            ## Inicio Gazeta
            for gpTitulo in response['Gazeta_do_povo']:
                s2 = nlp(gpTitulo['dados']['titulo'])
                Similaridade.append({'Similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': gpTitulo['dados']['titulo'], 'Link_Noticia': gpTitulo['dados']['Link']}, 'site_name':'Gazeta_do_povo'})
            
            gazetaSimilar = list(filter(lambda x:x['site_name'] == 'Gazeta_do_povo', Similaridade))
            i = 0
            for gpSubtitulo in response['Gazeta_do_povo']:
                s2 = nlp(gpSubtitulo['dados']['subtitulo'])

                gazetaSimilar[i]['Similaridade']['subtitulo'] = f"{round(s1.similarity(s2)* 100, 2)}"
                gazetaSimilar[i]['Similaridade']['subtitulo_original'] = gpSubtitulo['dados']['subtitulo']
                i += 1
            ## Fim Gazeta
            ## Inicio Estadao
            
            for estadaotitulo in response['Estadao']:
                s2 = nlp(estadaotitulo['dados']['titulo'])
                Similaridade.append({'Similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': estadaotitulo['dados']['titulo'], 'Link_Noticia': estadaotitulo['dados']['Link']}, 'site_name':'Estadao'})
            
            estadaoSimilar = list(filter(lambda x:x['site_name'] == 'Estadao', Similaridade))
            i = 0
            for estadaoSubtitulo in response['Estadao']:
                s2 = nlp(estadaoSubtitulo['dados']['subtitulo'])
                estadaoSimilar[i]['Similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}"
                estadaoSimilar[i]['Similaridade']['subtitulo_original'] = estadaoSubtitulo['dados']['subtitulo']
                i+= 1

            return {
                'Folha_de_SaoPaulo': {
                    'titulo_mais_similar': [] if folhaSimiliar  == [] else max(folhaSimiliar, key=lambda x: x['Similaridade']['titulo'])['Similaridade'],
                    'subtitulo_mais_similar': [] if folhaSimiliar == [] else max(folhaSimiliar, key=lambda x: x['Similaridade']['subtitulo'])['Similaridade']
                },
                'Gazeta_do_povo': {
                    'titulo_mais_similar': [] if gazetaSimilar  == [] else max(gazetaSimilar, key=lambda x: x['Similaridade']['titulo'])['Similaridade'],
                    'subtitulo_mais_similar': [] if gazetaSimilar  == [] else max(gazetaSimilar, key=lambda x: x['Similaridade']['subtitulo'])['Similaridade']
                },
                'G1': {
                    'titulo_mais_similar': [] if g1Similar == [] else max(g1Similar, key=lambda x:x['Similaridade']['titulo'])['Similaridade'],
                    'subtitulo_mais_similar':  [] if g1Similar == [] else max(g1Similar, key=lambda x: x['Similaridade']['subtitulo'])['Similaridade']
                },
                'Estadao': {
                    'titulo_mais_similar': [] if estadaoSimilar == [] else max(estadaoSimilar, key=lambda x:x['Similaridade']['titulo'])['Similaridade'],
                    'subtitulo_mais_similar': [] if estadaoSimilar == [] else max(estadaoSimilar, key=lambda x:x['Similaridade']['subtitulo'])['Similaridade']
                }
            }
        except Exception as e:
            print('achei?')
            print(e)
            return e
    
    def SentimentAnalisys(self): ## Aqui analisaremos a emoção de cada texto, onde utilizaremos Neutro, Positivo e Negativo para avaliar
        nltk.download('vader_lexicon')
        try:
            response = self.GetCorpus()
            
            ## Folha de Sao Paulo
            s1 = rq[0]['Folha_de_sao_paulo']['Corpus']
            folhaCorpusSentiment = SentimentIntensityAnalyzer().polarity_scores(s1)
            
            ## Gazeta do Povo
            s2 = rq[0]['Gazeta_do_povo']['Corpus']
            gazetaCorpusSentiment = SentimentIntensityAnalyzer().polarity_scores(s2)

            ## G1
            s3 = rq[0]['G1']['Corpus']
            g1CorpusSentiment = SentimentIntensityAnalyzer().polarity_scores(s3)
            
            ## Metropoles

            s4 = rq[0]['Metropoles']['Corpus']
            metropolesSentiment = SentimentIntensityAnalyzer().polarity_scores(s4)

            ## UOL

            s5 = rq[0]['UOL']['Corpus']
            uolSentiment = SentimentIntensityAnalyzer().polarity_scores(s5)

            ## Estadao

            s6 = rq[0]['Estadao']['Corpus']
            estadaoSentiment = SentimentIntensityAnalyzer().polarity_scores(s6)

            print(f"Folha de Sao Paulo artigo: {folhaCorpusSentiment}")
            print(f"Gazeta do Povo artigo: {gazetaCorpusSentiment}")
            print(f"G1 artigo: {g1CorpusSentiment}")
            print(f"Metropoles artigo: {metropolesSentiment}")
            print(f"UOL artigo: {uolSentiment}")
            print(f"Estadao artigo: {estadaoSentiment}")

            return {
                'Folha_de_sao_paulo':{
                    'negativo': f"{round(folhaCorpusSentiment['neg']*100,2)}%",
                    'neutro': f"{round(folhaCorpusSentiment['neu']*100,2)}%",
                    'positivo': f"{round(folhaCorpusSentiment['pos']*100,2)}%"
                },
                'Gazeta_do_povo':{
                    'negativo': f"{round(gazetaCorpusSentiment['neg']*100, 2)}%",
                    'neutro': f"{round(gazetaCorpusSentiment['neu']*100, 2)}%",
                    'positivo': f"{round(gazetaCorpusSentiment['pos']*100, 2)}"
                },
                'G1': {
                    'negativo': f"{round(g1CorpusSentiment['neg']*100, 2)}%",
                    'neutro': f"{round(g1CorpusSentiment['neu']*100, 2)}%",
                    'positivo': f"{round(g1CorpusSentiment['pos']*100, 2)}%"
                },
                'Metropoles': {
                    'negativo': f"{round(metropolesSentiment['neg']*100, 2)}%",
                    'neutro': f"{round(metropolesSentiment['neu']*100, 2)}%",
                    'positivo': f"{round(metropolesSentiment['pos']*100, 2)}%"
                },
                'UOL': {
                    'negativo': f"{round(uolSentiment['neg']*100, 2)}%",
                    'neutro': f"{round(uolSentiment['neu']*100, 2)}%",
                    'positivo': f"{round(uolSentiment['pos']*100, 2)}%"
                },
                'Estadao': {
                    'negativo': f"{round(estadaoSentiment['neg']*100, 2)}%",
                    'neutro': f"{round(estadaoSentiment['neu']*100, 2)}%",
                    'positivo': f"{round(estadaoSentiment['pos']*100, 2)}%"
                }
            }
        except Exception as e:
            print('aqui 2')
            print(e)
            return e
    
    def GetCorpus(self): ## Aqui pegamos o corpo da notícia que é mais adequada com o que se é pesquisado pelo usuário
        try:
            Corpus = []
            urls = []
            
            data = self.GetSimilarity()
            for links in data:
                urls.append({'dados':{'titulo_link':data[links]['titulo_mais_similar']['Link_Noticia'], 'subtitulo_link':data[links]['subtitulo_mais_similar']['Link_Noticia']}, 'site_name':links})

            req = [grequests.get(link['dados']['titulo_link']) for link in urls]
            responses = grequests.map(req, size=4)
            for response in responses:
                print(f"Corpus-status_code: {response.status_code}")
                
                soup = BeautifulSoup(response.content, 'html.parser')

                ## Folha
                
                for item in urls:
                    i = 0
                    fullcorpus = ''
                    if item['site_name'] == 'Folha_de_SaoPaulo':
                        for fbody in soup.find_all(class_='c-news__body'):
                            while(i < len(fbody.find_all('p'))):
                                fullcorpus += fbody.find_all('p')[i].get_text().strip()
                                i += 1
                        Corpus.append({'site_name':item['site_name'], 'Corpus':fullcorpus})
                    
                    if item['site_name'] == 'Gazeta_do_povo':
                        ## Gazeta
                        i = 0
                        fullcorpus = ''
                        for gaBody in soup.find_all(class_='wrapper'):
                            while (i < len(gaBody.find_all('p'))):
                                fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                                i += 1
                        Corpus.append({'site_name':item['site_name'], 'Corpus': fullcorpus})

                    if item['site_name'] == 'G1':
                        ## G1
                        i = 0
                        fullcorpus = ''
                        g1link = ''

                        for originalLink in soup.find('script'):
                            g1link = originalLink.format().rsplit('window.location.replace("')[1].rsplit('");')[0]
                            
                        reqCorpus = grequests.get(g1link) ## -> Os links do G1 tem um problema para serem feitos requests, pois acaba dando erro e nesse erro está o link correto
                        response = grequests.map(reqCorpus)
                        for res in response:
                            print(f"g1 status_code: {res.status_code}")
                            soup = BeautifulSoup(res.content, 'html.parser')
                            for g1body in soup.find_all(class_='wall protected-content'):
                                while (i < len(g1body.find_all('p'))):
                                    fullcorpus += g1body.find_all('p')[i].get_text().strip()
                                    i += 1
                            Corpus.append({'site_name':item['site_name'], 'Corpus':fullcorpus})

                    if item['site_name'] == 'Estadao':
                        ## Estadao
                        i = 0
                        fullcorpus = ''

                        for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                            while(i < len(estadobody.find_all('p'))):
                                fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                                i += 1
                        Corpus.append({'site_name':item['site_name'], 'Corpus': fullcorpus})

            return {'Folha_de_sao_paulo':list(filter(lambda x: x['site_name'] == 'Folha_de_SaoPaulo', Corpus)), 'Gazeta_do_povo':list(filter(lambda x: x['site_name'] == 'Gazeta_do_povo', Corpus)), 'G1': list(filter(lambda x: x['site_name'] == 'G1', Corpus)), 'Estadao': list(filter(lambda x: x['site_name'] == 'Estadao', Corpus))}, 200
        except Exception as e:
            print('ou sera aqui?')
            print(e)
            return e

    def GetContentGoogleSearch (self, url):
        ## O url precisa seguir o padrao do metropoles e do UOL
        if url == '':
            return {'msg':'nao foi possivel concluir a requisicacao'}

        api_key = url.split('callback=')[1].split('&')[0]
        print(f"api_key: {api_key}")
        try:
            rq = requests.get(url, params={'q':self.newstoSearch.replace(' ','+')})
            print(f"status_code_first_attemp: {rq.status_code}")
            if rq.status_code == 200:
                htmlcontent = rq.text.split('/*O_o*/')[1].split(str(api_key)+'(')[1].split(');')[0]
                print(htmlcontent[2:7])
                if htmlcontent[2:7] == 'error':
                    return {'dados':self.MultiConnectionsWithProxy(url, api_key)}
                else:
                    return {'dados':json.loads(htmlcontent)}
        except Exception as e:
            print(e)
            return {'msg':'Nao foi possivel finalizar a requisicao, por favor tente novamente!'}

    def MultiConnectionsWithProxy(self, url, api_key):
        rq = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=https&country=BR&timeout=3000&proxy_format=ipport&format=json')
        if rq.status_code == 200:
            print(f"proxy_requisition: {rq.status_code}")
            for i in rq.json()['proxies']:
                try:
                    print(f"proxy: {i['proxy']}; protocol: {i['protocol']}")
                    rq = requests.get(url, params={'q':self.newstoSearch.replace(' ','+')}, proxies={'https':i['proxy'], 'http': i['proxy']}, timeout=15)
                    print(f"status_code: {rq.status_code}")
                    if rq.status_code == 200:
                        # print(rq.text.split('/*O_o*/')[1].split(str(api_key)+'(')[1].split(');')[0]) ## ate agora funcionando como o esperado
                        htmlcontent = rq.text.split('/*O_o*/')[1].split(str(api_key)+'(')[1].split(');')[0]
                        return htmlcontent
                except requests.exceptions.RequestException as e:
                    print(e)