import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import grequests
from bs4 import BeautifulSoup
import spacy

class Scraper:
    def __init__(self, newstoSearch):
        self.newstoSearch = newstoSearch

    def GetData(self):  ## Aqui a gente vai utilizar para "pegar" os titulos, manchetes e os links de cada noticia
        if self.newstoSearch == "":
            return {'msg': 'Você está fazendo uma requisição, mas não cumprindo com todos os requisitos!', 'finished': False, 'error': True}, 200
        
        data = []
        searchEngineStandart = [ ## Sites que utilizam a mesma syntax para realizar pesquisas. Ou seja, utilizando *q=* significando query ou pesquisa traduzindo ao pe da letra
            'https://g1.globo.com/busca/?order=recent&species=notícias&', 
            #G1
            
            'https://search.folha.uol.com.br/?periodo=mes&site=todos&',
            # Folha de São Paulo

            'https://www.gazetadopovo.com.br/busca/?sort=newest&period=last-year&',
            # Gazeta do Povo

            'https://busca.estadao.com.br/?tipo_conteudo=Todos&quando=no-ultimo-mes&',
            # Estadao   
        ]

        try:

            req = [grequests.get(str(url) + 'q=' + self.newstoSearch.replace(" ", "+")) for url in searchEngineStandart]
            responses = grequests.map(req, size=2)
            g1 = []
            folha = []
            estadao = []
            gp = []

            for response in responses:
                print(f"get_data: {response.status_code}")
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
                'gazeta_do_povo': gp,
                'g1': g1,
                'estadao': estadao,
            }
        except Exception as e:
            print(e)
            return {'msg':'não foi possível completar a tarefa, por favor tente novamente!'}

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

                gazetaSimilar[i]['similaridade']['subtitulo'] = f"{round(s1.similarity(s2)* 100, 2)}%"
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
                estadaoSimilar[i]['similaridade']['subtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
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
            return {'msg':'Ocorreu um erro ao tentar completar a ação. Por favor tente novamente!'}
    
    def SentimentAnalisys(self): ## Aqui analisaremos a emoção de cada texto, onde utilizaremos Neutro, Positivo e Negativo para avaliar
        nltk.download('vader_lexicon')
        try:
            response = self.GetCorpus()
            if response == []:
                return []

            sentiment = []

            ## Folha de Sao Paulo
            folha_title = response['folha_de_saopaulo']['title_based']
            folha_sub = response['folha_de_saopaulo']['subtitle_based']
            sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(folha_title), 'subtitle': SentimentIntensityAnalyzer().polarity_scores(folha_sub), 'origin':'folha_de_saopaulo'})
            
            ## Gazeta do Povo
            gazeta_title = response['gazeta_do_povo']['title_based']
            gazeta_sub = response['gazeta_do_povo']['subtitle_based']
            sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(gazeta_title), 'subtitle': SentimentIntensityAnalyzer().polarity_scores(gazeta_sub), 'origin':'gazeta_do_povo'})

            ## G1
            g1_title = response['g1']['title_based']
            g1_sub = response['g1']['subtitle_based']
            sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(g1_title), 'subtitle': SentimentIntensityAnalyzer().polarity_scores(g1_sub), 'origin':'g1'})

            ## Estadao

            estadao_title = response['estadao']['title_based']
            estadao_sub = response['estadao']['subtitle_based']
            sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(estadao_title), 'subtitle': SentimentIntensityAnalyzer().polarity_scores(estadao_sub), 'origin':'estadao'})

            return {
                'folha_de_saopaulo':{
                    'title_based': {
                        # 'negativo': f"{round(folhaCorpusSentiment['neg']*100,2)}%",
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['title']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['title']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['title']['pos']*100,2) if sentiment else []}%",
                    },
                    'subtitle_based': {
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['subtitle']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['subtitle']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['subtitle']['pos']*100,2) if sentiment else []}%",
                    }
                },
                'gazeta_do_povo':{
                    'title_based': {
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['title']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['title']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['title']['pos']*100,2) if sentiment else []}%",
                    },
                    'subtitle_based':{
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['subtitle']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['subtitle']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['subtitle']['pos']*100,2) if sentiment else []}%",
                    }
                },
                'g1': {
                    'title_based':{
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['title']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['title']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['title']['pos']*100,2) if sentiment else []}%",
                    },
                    'subtitle_based':{
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['subtitle']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['subtitle']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['subtitle']['pos']*100,2) if sentiment else []}%",
                    }
                },
                'estadao': {
                    'title_based':{
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['title']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['title']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['title']['pos']*100,2) if sentiment else []}%",
                    },
                    'subtitle_based':{
                        'negativo': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['subtitle']['neg']*100,2) if sentiment else []}%",
                        'neutro': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['subtitle']['neu']*100,2) if sentiment else []}%",
                        'positivo': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['subtitle']['pos']*100,2) if sentiment else []}%",
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
                if data[site_origin]['titulo_mais_similar'] == [] and data[site_origin]['subtitulo_mais_similar'] == []:
                    return []
                
                url_titlebased.append({'site_origin':site_origin, 'link': data[site_origin]['titulo_mais_similar']['link_noticia']})
                url_subtitlebased.append({'site_origin': site_origin, 'link': data[site_origin]['subtitulo_mais_similar']['link_noticia']})

            ## Start first with title link's based

            title_request = [grequests.get(link['link']) for link in url_titlebased]
            title_response = grequests.map(title_request, size=4)
            subtitle_request = [grequests.get(link['link']) for link in url_subtitlebased]
            subtitle_response = grequests.map(subtitle_request, size=4)

            for response in title_response:
                print(f"title get_corpus: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')

                ## Folha

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'folha_de_saopaulo' for index in corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url_titlebased]):
                    for fbody in soup.find_all(class_='c-news__body'):
                        while(i < len(fbody.find_all('p'))):
                            fullcorpus += fbody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus':fullcorpus, 'site_origin':'folha_de_saopaulo'})
                
                ## Gazeta

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'gazeta_do_povo' for index in corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in url_titlebased]):
                    for gaBody in soup.find_all(class_='wrapper'):
                        while (i < len(gaBody.find_all('p'))):
                            fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus': fullcorpus, 'site_origin':'gazeta_do_povo'})
                
                ## G1

                i = 0
                fullcorpus = ''
                g1link = []
                if (any([index['site_origin'] == 'g1' for index in corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'g1' for index in url_titlebased]):
                    for originalLink in soup.find('script'):
                        if 'window.location.replace' in originalLink:
                            g1link.append({'g1_link':originalLink.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})

                    reqCorpus = [grequests.get(g1_url['g1_link']) for g1_url in g1link] ## -> Os links do G1 tem um problema para serem feitos requests, pois acaba dando erro e nesse erro está o link correto
                    g1_res = grequests.map(reqCorpus, size=1)
                    for g1_response in g1_res:
                        print(f"title get_corpus --> g1 / status_code: {g1_response.status_code}")
                        soup = BeautifulSoup(g1_response.content, 'html.parser')

                        for g1body in soup.find_all(class_='wall protected-content'):
                            while (i < len(g1body.find_all('p'))):
                                fullcorpus += g1body.find_all('p')[i].get_text().strip()
                                i += 1
                        corpus.append({'corpus':fullcorpus, 'site_origin':'g1'})

                ## Estadao

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'estadao' for index in corpus]) == False) and  any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in url_titlebased]):
                    for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                        while(i < len(estadobody.find_all('p'))):
                            fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus': fullcorpus,'site_origin':'estadao'})
            
            ## get_corpus related to the subtitle

            for response in subtitle_response:
                print(f"subtitle get_corpus: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')

                ## Folha

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'folha_de_saopaulo' for index in subtitle_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url_subtitlebased]):
                    for fbody in soup.find_all(class_='c-news__body'):
                        while(i < len(fbody.find_all('p'))):
                            fullcorpus += fbody.find_all('p')[i].get_text().strip()
                            i += 1
                    subtitle_corpus.append({'corpus':fullcorpus, 'site_origin':'folha_de_saopaulo'})
                
                ## Gazeta

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'gazeta_do_povo' for index in subtitle_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in url_subtitlebased]):
                    for gaBody in soup.find_all(class_='wrapper'):
                        while (i < len(gaBody.find_all('p'))):
                            fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                            i += 1
                    subtitle_corpus.append({'corpus': fullcorpus, 'site_origin':'gazeta_do_povo'})
                
                ## G1

                i = 0
                fullcorpus = ''
                subtitle_g1link = []
                if (any([index['site_origin'] == 'g1' for index in subtitle_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'g1' for index in url_subtitlebased]):
                    for originalLink in soup.find('script'):
                        if 'window.location.replace' in originalLink:
                            subtitle_g1link.append({'g1_link':originalLink.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})

                    subtitle_g1_request = [grequests.get(g1_url['g1_link']) for g1_url in subtitle_g1link] ## -> Os links do G1 tem um problema para serem feitos requests, pois acaba dando erro e nesse erro está o link correto
                    g1_sub_response = grequests.map(subtitle_g1_request, size=1)

                    for g1_response in g1_sub_response:
                        print(f"subtitle get_corpus --> g1 / status_code: {g1_response.status_code}")
                        soup = BeautifulSoup(g1_response.content, 'html.parser')

                        for g1body in soup.find_all(class_='wall protected-content'):
                            while (i < len(g1body.find_all('p'))):
                                fullcorpus += g1body.find_all('p')[i].get_text().strip()
                                i += 1
                        subtitle_corpus.append({'corpus':fullcorpus, 'site_origin':'g1'})

                ## Estadao
                
                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'estadao' for index in subtitle_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in url_subtitlebased]):
                    for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                        while(i < len(estadobody.find_all('p'))):
                            fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                            i += 1
                    subtitle_corpus.append({'corpus': fullcorpus,'site_origin':'estadao'})
            
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
                'estadao':{
                    'title_based': list(filter(lambda x:x['site_origin'] == 'estadao', corpus))[0]['corpus'] if corpus else [],
                    'subtitle_based': list(filter(lambda x:x['site_origin'] == 'estadao', subtitle_corpus))[0]['corpus'] if subtitle_corpus else [],
                }
            }
        except Exception as e:
            print('ou sera aqui?')
            return e
    
    def get_date(self):
        try:
            content = self.GetSimilarity()
            title_url = []
            subtitle_url = []
            date_corpus= []

            for index in content:
                if content[index]['titulo_mais_similar'] ==  [] and content[index]['subtitulo_mais_similar'] ==  []:
                    return []

                title_url.append({'link':content[index]['titulo_mais_similar']['link_noticia'], 'site_origin':index})
                subtitle_url.append({'link':content[index]['subtitulo_mais_similar']['link_noticia'], 'site_origin': index})

            date_title_request = [grequests.get(link['link']) for link in title_url]
            date_responses = grequests.map(date_title_request, size=4)
            
            date_sub_request = [grequests.get(link['link']) for link in subtitle_url]
            date_sub_responses = grequests.map(date_sub_request, size=4)

            # Primeiro comecaremos com o titulo

            for response in date_responses:
                print(f"title get_date: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')

                #Folha de Sao Paulo
                if (any([index['site_origin'] == 'folha_de_saopaulo' and index['to'] == 'title' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in title_url]):
                    for folha_date in soup.find(class_='c-more-options__published-date'):
                        date_corpus.append({'datetime':folha_date.get_text().strip(), 'site_origin':'folha_de_saopaulo','to':'title', 'origin': response.url})

                #Gazeta do povo
                if (any([index['site_origin'] == 'gazeta_do_povo' and index['to'] == 'title' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in title_url]):
                    for gazeta_date in soup.find(class_='wgt-date'):
                        date_corpus.append({'datetime':gazeta_date.get_text().strip(), 'site_origin':'gazeta_do_povo','to':'title', 'origin': response.url})
                
                #G1
                formatt_link = []
                if (any([index['site_origin'] == 'g1' and index['to'] == 'title' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'g1' for index in title_url]):
                    for getscript in soup.find('script'):
                        if 'window.location.replace' in getscript:
                            formatt_link.append({'link':getscript.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})
                            
                    g1format_rq = [grequests.get(link['link']) for link in formatt_link]
                    g1format_res = grequests.map(g1format_rq, size=1)
                    for g1response in g1format_res:
                        print(f"title get_date g1 : {g1response.status_code}")
                        soup = BeautifulSoup(g1response.content, 'html.parser')

                        for g1date in soup.find(class_='content-publication-data__updated'):
                            date_corpus.append({'datetime':g1date.find_next('time').get_text().strip(), 'site_origin':'g1', 'to':'title', 'origin': response.url})
                            break

                #Estadao
                if (any([index['site_origin'] == 'estadao' and index['to'] == 'title' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in title_url]):
                    for estadao_date in soup.find(class_='principal-dates'):
                        date_corpus.append({'datetime':estadao_date.find_next('time').get_text().strip(), 'site_origin':'estadao', 'to':'title', 'origin': response.url})
                        break
            
            # Agora realiza a busca pela as datas com base no subtitulo

            for response in date_sub_responses:
                print(f"subtitle get_data: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')

                #Folha de sao paulo

                if (any([index['site_origin'] == 'folha_de_saopaulo' and index['to'] == 'subtitle' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in subtitle_url]):
                    for folha_date in soup.find(class_='c-more-options__published-date'):
                        date_corpus.append({'datetime':folha_date.get_text().strip(), 'site_origin':'folha_de_saopaulo','to':'subtitle', 'origin': response.url})
                
                #Gazeta do povo

                if (any([index['site_origin'] == 'gazeta_do_povo' and index['to'] == 'subtitle' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in subtitle_url]):
                    for gazeta_date in soup.find(class_='wgt-date'):
                        date_corpus.append({'datetime':gazeta_date.get_text().strip(), 'site_origin':'gazeta_do_povo','to':'subtitle', 'origin': response.url})
                
                # G1

                formatt_link_sub = []
                if (any([index['site_origin'] == 'g1' and index['to'] == 'subtitle' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'g1' for index in subtitle_url]):
                    for getscript in soup.find('script'):
                        if 'window.location.replace' in getscript:
                            formatt_link_sub.append({'link':getscript.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})
                            
                    g1formatsub_rq = [grequests.get(link['link']) for link in formatt_link_sub]
                    g1formatsub_res = grequests.map(g1formatsub_rq, size=1)
                    for g1response in g1formatsub_res:
                        print(f"title get_date g1 : {g1response.status_code}")
                        soup = BeautifulSoup(g1response.content, 'html.parser')

                        for g1date in soup.find(class_='content-publication-data__updated'):
                            date_corpus.append({'datetime':g1date.find_next('time').get_text().strip(), 'site_origin':'g1', 'to':'subtitle', 'origin': response.url})
                            break

                #Estadao
                
                if (any([index['site_origin'] == 'estadao' and index['to'] == 'subtitle' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in subtitle_url]):
                    for estadao_date in soup.find(class_='principal-dates'):
                        date_corpus.append({'datetime':estadao_date.find_next('time').get_text().strip(), 'site_origin':'estadao', 'to':'subtitle', 'origin': response.url})
                        break
            return {
                'folha_de_saopaulo':{
                    'title_based':list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo' and x['to'] == 'title', date_corpus))[0] if date_corpus else [],
                    'subtitle_based':list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo' and x['to'] == 'subtitle',  date_corpus))[0] if date_corpus else []
                },
                'gazeta_do_povo':{
                    'title_based':list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo' and x['to'] == 'title', date_corpus))[0] if date_corpus else [],
                    'subtitle_based':list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo' and x['to'] == 'subtitle',  date_corpus))[0] if date_corpus else []
                },
                'g1':{
                    'title_based':list(filter(lambda x:x['site_origin'] == 'g1' and x['to'] == 'title', date_corpus))[0] if date_corpus else [],
                    'subtitle_based':list(filter(lambda x:x['site_origin'] == 'g1' and x['to'] == 'subtitle',  date_corpus))[0] if date_corpus else []
                },
                'estadao': {
                    'title_based':list(filter(lambda x:x['site_origin'] == 'estadao' and x['to'] == 'title', date_corpus))[0] if date_corpus else [],
                    'subtitle_based':list(filter(lambda x:x['site_origin'] == 'estadao' and x['to'] == 'subtitle',  date_corpus))[0] if date_corpus else []
                }
            }
        except Exception as e:
            print(e)
            return e