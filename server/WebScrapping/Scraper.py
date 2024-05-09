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
            'https://g1.globo.com/busca/?order=recent&species=notícias&', 
            #G1
            'https://search.folha.uol.com.br/?site=todos&',
            # Folha de São Paulo
            'https://www.gazetadopovo.com.br/busca/?', ## Utiliza q
            # Gazeta do Povo
            'https://busca.estadao.com.br/?',
            # Estadao
            
        ]
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
                    data.append({'site_url':searchEngineStandart[0], 'site_name':'g1', 'dados':{'titulo':gTitulo.get_text().strip()}})
                g1 = list(filter(lambda x: x['site_name'] == 'g1', data))
                i = 0
                for gSubtitulo in soup.find_all(class_='widget--info__description'):
                    if i < len(g1):
                        g1[i]['dados']['subtitulo'] = gSubtitulo.get_text().strip()
                        i+= 1
                i = 0
                for gLink in soup.find_all(class_='widget--info__text-container'):
                    if i < len(g1):
                        g1[i]['dados']['link'] = "https:"+gLink.find('a').get('href')
                        i+= 1
                ##fim g1
                ##inicio folha
                for fTitulo in soup.find_all(class_='c-headline__title'):
                    data.append({'site_url':searchEngineStandart[1], 'site_name':'folha_de_sao_paulo', 'dados': {'titulo':fTitulo.get_text().strip()}})
                folha = list(filter(lambda x: x['site_name'] == 'folha_de_sao_paulo', data))
                i = 0
                for fSubtitulo in soup.find_all(class_='c-headline__standfirst'):
                    if fSubtitulo.get_text().strip() != 'O jornal Folha de S.Paulo é publicado pela Empresa Folha da Manhã S.A. CNPJ: 60.579.703/0001-48' and i < len(folha):
                        folha[i]['dados']['subtitulo'] = fSubtitulo.get_text().strip()
                        i += 1
                i = 0
                for fLink in soup.find_all(class_='c-headline__content'):
                    if i < len(folha):
                        folha[i]['dados']['link'] = fLink.find('a').get('href')
                        i += 1
                ## Fim Folha
                ## Gazeta do Povo
                for gpTitulo in soup.find_all(class_='post-title'):
                    data.append({'site_url': searchEngineStandart[2], 'site_name':'gazeta_do_povo', 'dados':{'titulo': gpTitulo.get_text().strip()}})
                gp = list(filter(lambda x: x['site_name'] == 'gazeta_do_povo', data))
                i = 0
                for gpSubtitulo in soup.find_all(class_='post-summary'):
                    if i < len(gp):
                        gp[i]['dados']['subtitulo'] = gpSubtitulo.get_text().strip()
                        i += 1
                i = 0
                for gpLink in soup.find_all(class_='post-url'):
                    if i < len(gp):
                        gp[i]['dados']['link'] = gpLink.get('href')
                        i += 1
                ## Fim Gazeta
                ## Estadao
                for estadoTitulo in soup.find_all(class_='link-title'):
                    data.append({'site_url':searchEngineStandart[3], 'site_name':'estadao', 'dados':{'titulo': estadoTitulo.find('h3').get_text().strip(), 'link': estadoTitulo.get('href')}})
                
                estadao = list(filter(lambda x: x['site_name'] == 'estadao', data))
                i = 0
                for estadoSubtitulo in soup.find_all(class_='link-title'):
                    for item in estadoSubtitulo.find_all('p'):
                        if i < len(estadao):
                            estadao[i]['dados']['subtitulo'] = "Nao possui subtitulo" if item.get_text().strip() == '' else item.get_text().strip()
                            i += 1
            
            return {
                'folha_de_sao_paulo': folha,
                'g1': g1,
                'estadao': estadao,
                'gazeta_do_povo': gp
            }
        except Exception as e:
            print(e)

    def GetSimilarity(self): ## Após "pegar" as informações de um conjunto de notícias, precisamos agora análisar cada titulo e subtitulo para ver qual notícia é mais adequada com o que o usuário pesquisou
        similaridade = []

        try:
            response = self.GetData()
            ## Inicio G1
            nlp = spacy.load('pt_core_news_lg') ## Para carregar o pacote que usaremos para analisar os titulos e as manchetes
            s1 = nlp(self.newstoSearch) ## Cria um objeto com as informações estruturais gramaticais e semânticas do texto

            for gTitulo in response['g1']:
                s2 = nlp(gTitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': gTitulo['dados']['titulo'], 'link_noticia': gTitulo['dados']['link']}, 'site_name':'g1'})

            g1Similar = list(filter(lambda x: x['site_name'] == 'g1', similaridade))
            i = 0
            for gSubtitulo in response['g1']:
                s2 = nlp(gSubtitulo['dados']['subtitulo'])

                g1Similar[i]['similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                g1Similar[i]['similaridade']['subtitulo_original'] = gSubtitulo['dados']['subtitulo']
                i += 1
            ## fim g1
            ## Inicio Folha
            for fTitulo in response['folha_de_sao_paulo']:
                s2 = nlp(fTitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': fTitulo['dados']['titulo'], 'link_noticia': fTitulo['dados']['link']}, 'site_name':'folha_de_sao_paulo'})

            folhaSimiliar = list(filter(lambda x: x['site_name'] == 'folha_de_sao_paulo', similaridade))
            i=0
            for fSubtitulo in response['folha_de_sao_paulo']:
                s2 = nlp(fSubtitulo['dados']['subtitulo'])

                folhaSimiliar[i]['similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                folhaSimiliar[i]['similaridade']['subtitulo_original'] = fSubtitulo['dados']['subtitulo']
                i += 1

            ## Fim Folha
            ## Inicio Gazeta
            for gpTitulo in response['gazeta_do_povo']:
                s2 = nlp(gpTitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': gpTitulo['dados']['titulo'], 'link_noticia': gpTitulo['dados']['link']}, 'site_name':'gazeta_do_povo'})
            
            gazetaSimilar = list(filter(lambda x:x['site_name'] == 'gazeta_do_povo', similaridade))
            i = 0
            for gpSubtitulo in response['gazeta_do_povo']:
                s2 = nlp(gpSubtitulo['dados']['subtitulo'])

                gazetaSimilar[i]['similaridade']['subtitulo'] = f"{round(s1.similarity(s2)* 100, 2)}"
                gazetaSimilar[i]['similaridade']['subtitulo_original'] = gpSubtitulo['dados']['subtitulo']
                i += 1
            ## Fim Gazeta
            ## Inicio Estadao
            
            for estadaotitulo in response['estadao']:
                s2 = nlp(estadaotitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': f"{round(s1.similarity(s2)*100, 2)}%", 'titulo_original': estadaotitulo['dados']['titulo'], 'link_noticia': estadaotitulo['dados']['link']}, 'site_name':'estadao'})
            
            estadaoSimilar = list(filter(lambda x:x['site_name'] == 'estadao', similaridade))
            i = 0
            for estadaoSubtitulo in response['estadao']:
                s2 = nlp(estadaoSubtitulo['dados']['subtitulo'])
                estadaoSimilar[i]['similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}"
                estadaoSimilar[i]['similaridade']['subtitulo_original'] = estadaoSubtitulo['dados']['subtitulo']
                i+= 1

            return {
                'folha_de_saopaulo': {
                    'titulo_mais_similar': [] if folhaSimiliar  == [] else max(folhaSimiliar, key=lambda x: x['similaridade']['titulo'])['similaridade'],
                    'subtitulo_mais_similar': [] if folhaSimiliar == [] else max(folhaSimiliar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']
                },
                'gazeta_do_povo': {
                    'titulo_mais_similar': [] if gazetaSimilar  == [] else max(gazetaSimilar, key=lambda x: x['similaridade']['titulo'])['similaridade'],
                    'subtitulo_mais_similar': [] if gazetaSimilar  == [] else max(gazetaSimilar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']
                },
                'g1': {
                    'titulo_mais_similar': [] if g1Similar == [] else max(g1Similar, key=lambda x:x['similaridade']['titulo'])['similaridade'],
                    'subtitulo_mais_similar':  [] if g1Similar == [] else max(g1Similar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']
                },
                'estadao': {
                    'titulo_mais_similar': [] if estadaoSimilar == [] else max(estadaoSimilar, key=lambda x:x['similaridade']['titulo'])['similaridade'],
                    'subtitulo_mais_similar': [] if estadaoSimilar == [] else max(estadaoSimilar, key=lambda x:x['similaridade']['subtitulo'])['similaridade']
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
            ## s1, s2... Mean sentence.

            ## Folha de Sao Paulo
            s1 = response['folha_de_saopaulo']
            folhaCorpusSentiment = SentimentIntensityAnalyzer().polarity_scores(s1)
            
            ## Gazeta do Povo
            s2 = response['gazeta_do_povo']
            gazetaCorpusSentiment = SentimentIntensityAnalyzer().polarity_scores(s2)

            ## G1
            s3 = response['g1']
            g1CorpusSentiment = SentimentIntensityAnalyzer().polarity_scores(s3)

            ## Estadao

            s6 = response['estadao']
            estadaoSentiment = SentimentIntensityAnalyzer().polarity_scores(s6)

            print(f"Folha de Sao Paulo artigo: {folhaCorpusSentiment}")
            print(f"Gazeta do Povo artigo: {gazetaCorpusSentiment}")
            print(f"G1 artigo: {g1CorpusSentiment}")
            print(f"Estadao artigo: {estadaoSentiment}")

            return {
                'folha_de_saopaulo':{
                    'noticia_baseada_titulo': {
                        'negativo': f"{round(folhaCorpusSentiment['neg']*100,2)}%",
                        'neutro': f"{round(folhaCorpusSentiment['neu']*100,2)}%",
                        'positivo': f"{round(folhaCorpusSentiment['pos']*100,2)}%"
                    }
                },
                'gazeta_do_povo':{
                    'noticia_baseada_titulo': {
                        'negativo': f"{round(gazetaCorpusSentiment['neg']*100, 2)}%",
                        'neutro': f"{round(gazetaCorpusSentiment['neu']*100, 2)}%",
                        'positivo': f"{round(gazetaCorpusSentiment['pos']*100, 2)}"
                    }
                },
                'g1': {
                    'noticia_baseada_titulo':{
                        'negativo': f"{round(g1CorpusSentiment['neg']*100, 2)}%",
                        'neutro': f"{round(g1CorpusSentiment['neu']*100, 2)}%",
                        'positivo': f"{round(g1CorpusSentiment['pos']*100, 2)}%"
                    }
                },
                'estadao': {
                    'noticia_baseada_titulo':{
                        'negativo': f"{round(estadaoSentiment['neg']*100, 2)}%",
                        'neutro': f"{round(estadaoSentiment['neu']*100, 2)}%",
                        'positivo': f"{round(estadaoSentiment['pos']*100, 2)}%"
                    }
                }
            }
        except Exception as e:
            print('aqui 2')
            print(e)
            return e
    
    def GetCorpus(self): ## Aqui pegamos o corpo da notícia que é mais adequada com o que se é pesquisado pelo usuário
        try:
            corpus = []
            subtitle_corpus = []
            url_subtitlebased = []
            url_titlebased = []

            data = self.GetSimilarity()

            for site_origin in data:
                url_titlebased.append({'site_origin':site_origin, 'link': data[site_origin]['titulo_mais_similar']['link_noticia']})
                url_subtitlebased.append({'site_origin': site_origin, 'link': data[site_origin]['subtitulo_mais_similar']['link_noticia']})

            ## Start first with title link's based

            print(url_titlebased)
            title_request = [grequests.get(link['link']) for link in url_titlebased]
            title_response = grequests.map(title_request, size=4)
            subtitle_request = [grequests.get(link['link']) for link in url_subtitlebased]
            subtitle_response = grequests.map(subtitle_request, size=4)

            for response in title_response:
                print(f"get corpus: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')
                # print(any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url_titlebased]) == True)
                print(any([len(content) == 0 for content in subtitle_corpus]))

                ## Folha
                i = 0
                fullcorpus = ''
                if any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url_titlebased]) and any([len(content['site_origin']) == 0 for content in corpus]):
                    for fbody in soup.find_all(class_='c-news__body'):
                        while(i < len(fbody.find_all('p'))):
                            fullcorpus += fbody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus':fullcorpus, 'site_origin':'folha_de_saopaulo'})
                
                ## Gazeta
                i = 0
                fullcorpus = ''
                if any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in url_titlebased]) and any([len(content['site_origin']) == 0 for content in corpus]):
                    for gaBody in soup.find_all(class_='wrapper'):
                        while (i < len(gaBody.find_all('p'))):
                            fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus': fullcorpus, 'site_origin':'gazeta_do_povo'})
                
                ## G1
                i = 0
                fullcorpus = ''
                g1link = []
                if any([index['link'] == response.url and index['site_origin'] == 'g1' for index in url_titlebased]) and any([len(content['site_origin']) == 0 for content in corpus]):
                    for originalLink in soup.find('script'):
                        if 'window.location.replace' in originalLink:
                            g1link.append({'g1_link':originalLink.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})

                    reqCorpus = [grequests.get(g1_url['g1_link']) for g1_url in g1link] ## -> Os links do G1 tem um problema para serem feitos requests, pois acaba dando erro e nesse erro está o link correto
                    g1_res = grequests.map(reqCorpus, size=1)
                    for g1_response in g1_res:
                        print(f"get_corpus --> g1 / status_code: {g1_response.status_code}")
                        soup = BeautifulSoup(g1_response.content, 'html.parser')

                        for g1body in soup.find_all(class_='wall protected-content'):
                            while (i < len(g1body.find_all('p'))):
                                fullcorpus += g1body.find_all('p')[i].get_text().strip()
                                i += 1
                        corpus.append({'corpus':fullcorpus, 'site_origin':'g1'})

                ## Estadao
                i = 0
                fullcorpus = ''
                if any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in url_titlebased]) and any([len(content['site_origin']) == 0 for content in corpus]):
                    for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                        while(i < len(estadobody.find_all('p'))):
                            fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus': fullcorpus,'site_origin':'estadao'})
            
            ## get_corpus related to the subtitle
            for response in subtitle_response:
                print(f"get corpus: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')
                print(any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url_subtitlebased]) == True)

                ## Folha
                i = 0
                fullcorpus = ''
                if any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url_subtitlebased]) and any([len(content['site_origin']) == 0 for content in subtitle_corpus]):
                    for fbody in soup.find_all(class_='c-news__body'):
                        while(i < len(fbody.find_all('p'))):
                            fullcorpus += fbody.find_all('p')[i].get_text().strip()
                            i += 1
                    subtitle_corpus.append({'corpus':fullcorpus, 'site_origin':'folha_de_saopaulo'})
                
                ## Gazeta
                i = 0
                fullcorpus = ''
                if any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in url_subtitlebased]) and any([len(content['site_origin']) == 0 for content in subtitle_corpus]):
                    for gaBody in soup.find_all(class_='wrapper'):
                        while (i < len(gaBody.find_all('p'))):
                            fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                            i += 1
                    subtitle_corpus.append({'corpus': fullcorpus, 'site_origin':'gazeta_do_povo'})
                
                ## G1
                i = 0
                fullcorpus = ''
                subtitle_g1link = []
                if any([index['link'] == response.url and index['site_origin'] == 'g1' for index in url_subtitlebased]) and any([len(content['site_origin']) == 0 for content in subtitle_corpus]):
                    for originalLink in soup.find('script'):
                        if 'window.location.replace' in originalLink:
                            subtitle_g1link.append({'g1_link':originalLink.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})

                    subtitle_g1_request = [grequests.get(g1_url['g1_link']) for g1_url in g1link] ## -> Os links do G1 tem um problema para serem feitos requests, pois acaba dando erro e nesse erro está o link correto
                    g1_sub_response = grequests.map(subtitle_g1_request, size=1)

                    for g1_response in g1_sub_response:
                        print(f"get_corpus --> g1 / status_code: {g1_response.status_code}")
                        soup = BeautifulSoup(g1_response.content, 'html.parser')

                        for g1body in soup.find_all(class_='wall protected-content'):
                            while (i < len(g1body.find_all('p'))):
                                fullcorpus += g1body.find_all('p')[i].get_text().strip()
                                i += 1
                        subtitle_corpus.append({'corpus':fullcorpus, 'site_origin':'g1'})

                ## Estadao
                i = 0
                fullcorpus = ''
                if any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in url_subtitlebased]) and any([len(content['site_origin']) == 0 for content in subtitle_corpus]):
                    for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                        while(i < len(estadobody.find_all('p'))):
                            fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                            i += 1
                    subtitle_corpus.append({'corpus': fullcorpus,'site_origin':'estadao'})
                # print(list(filter(lambda x:x['site_origin'] == 'g1', subtitle_corpus))[0]['corpus'] if subtitle_corpus else [])
                
                for i in subtitle_corpus:
                    print(i['corpus']) if i['site_origin'] == 'gazeta_do_povo' else []
            return {
                'folha_de_saopaulo':{
                    'title_based': list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo', corpus))[0]['corpus'] if corpus else [],
                    'subtitle_based': list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo', subtitle_corpus))[0]['corpus'] if subtitle_corpus else []
                },
                'gazeta_do_povo':{ 
                    'title_based': list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo', corpus))[0]['corpus'] if corpus else [],
                    'subtitle_based': list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo', subtitle_corpus))[0]['corpus'] if subtitle_corpus else []
                },
                'g1': {
                    'title_based': list(filter(lambda x:x['site_origin'] == 'g1', corpus))[0]['corpus'] if corpus else [],
                    'subtitle_based': list(filter(lambda x:x['site_origin'] == 'g1', subtitle_corpus))[0]['corpus'] if subtitle_corpus else [],
                },
                # 'estadao':{
                #     'title_based': list(filter(lambda x:x['site_origin'] == 'estadao', corpus))[0]['corpus'] if corpus else [],
                #     'subtitle_based': list(filter(lambda x:x['site_origin'] == 'estadao', subtitle_corpus))[0]['corpus'] if subtitle_corpus else [],
                # }
            }
        except Exception as e:
            print('ou sera aqui?')
            return e

    # def GetContentGoogleSearch (self, url):
    #     ## O url precisa seguir o padrao do metropoles e do UOL
    #     if url == '':
    #         return {'msg':'nao foi possivel concluir a requisicacao'}

    #     api_key = url.split('callback=')[1].split('&')[0]
    #     print(f"api_key: {api_key}")
    #     try:
    #         rq = requests.get(url, params={'q':self.newstoSearch.replace(' ','+')})
    #         print(f"status_code_first_attemp: {rq.status_code}")
    #         if rq.status_code == 200:
    #             htmlcontent = rq.text.split('/*O_o*/')[1].split(str(api_key)+'(')[1].split(');')[0]
    #             print(htmlcontent[2:7])
    #             if htmlcontent[2:7] == 'error':
    #                 return {'dados':self.MultiConnectionsWithProxy(url, api_key)}
    #             else:
    #                 return {'dados':json.loads(htmlcontent)}
    #     except Exception as e:
    #         print(e)
    #         return {'msg':'Nao foi possivel finalizar a requisicao, por favor tente novamente!'}

    # def MultiConnectionsWithProxy(self, url, api_key):
    #     rq = requests.get('https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=https&country=BR&timeout=3000&proxy_format=ipport&format=json')
    #     if rq.status_code == 200:
    #         print(f"proxy_requisition: {rq.status_code}")
    #         for i in rq.json()['proxies']:
    #             try:
    #                 print(f"proxy: {i['proxy']}; protocol: {i['protocol']}")
    #                 rq = requests.get(url, params={'q':self.newstoSearch.replace(' ','+')}, proxies={'https':i['proxy'], 'http': i['proxy']}, timeout=15)
    #                 print(f"status_code: {rq.status_code}")
    #                 if rq.status_code == 200:
    #                     # print(rq.text.split('/*O_o*/')[1].split(str(api_key)+'(')[1].split(');')[0]) ## ate agora funcionando como o esperado
    #                     htmlcontent = rq.text.split('/*O_o*/')[1].split(str(api_key)+'(')[1].split(');')[0]
    #                     return htmlcontent
    #             except requests.exceptions.RequestException as e:
    #                 print(e)