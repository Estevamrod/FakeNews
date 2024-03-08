import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
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
        searchEngineGoogle = [
            'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=pt-PT&source=gcsc&gss=.com&cselibv=8435450f13508ca1&cx=004590593083191455447%3A5j_p3qfagic&safe=off&cse_tok=AB-tC_7ewW0pO9BEfIR_jEBFa923%3A1709937160692&sort=&exp=cc%2Cdtsq-3&fexp=72497452&callback=google.search.cse.api5181&',
            # UOL
            'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=pt-BR&source=gcsc&gss=.br&cselibv=8435450f13508ca1&cx=33c20c29942ff412b&safe=off&cse_tok=AB-tC_6O_nEFvMPcLyCF3I43OvcT%3A1709937247606&lr=&cr=&gl=&filter=0&sort=&as_oq=&as_sitesearch=*.uol.com.br%2F*&exp=cc&fexp=72522726%2C72523582%2C72497452&callback=google.search.cse.api14043&',
            # Metropoles
        ]
        try:
            dadosG1 = {}
            dadosFolha = {}
            dadosGazeta = {}
            dadosEstadao = {}
            completeData= {}

            for url in searchEngineStandart:
                rs = requests.get(url, params={'q':self.newstoSearch.replace(" ", "+")})
                print(f"status code: {rs.status_code}")
                htmlcontent = rs.content
                i = 0 
                print(f'Actual url in request: {url}')
                soup = BeautifulSoup(htmlcontent, 'html.parser')
                ##inicio g1
                for gTitulo in soup.find_all(class_='widget--info__title product-color'):
                    # print(i.get_text())
                    dadosG1[i] = {
                        'site':url, 
                        'dados': {
                            'titulo': gTitulo.get_text().strip()
                        }
                        }
                    i += 1
                i = 0
                for gSubtitulo in soup.find_all(class_='widget--info__description'):
                    dadosG1[i]['dados']['subtitulo'] = gSubtitulo.get_text().strip()
                    i += 1
                i = 0
                for gLink in soup.find_all(class_='widget--info__text-container'):
                    # print(gLink.find('a').get('href'))
                    dadosG1[i]['dados']['Link'] = gLink.find('a').get('href')
                    i += 1
                ##fim g1
                ##inicio folha
                i = 0
                for fTitulo in soup.find_all(class_='c-headline__title'):
                    # print(fTitulo.get_text().strip())
                    dadosFolha[i] = {
                        'site':url,
                        'dados': {
                            'titulo': fTitulo.get_text().strip()
                        }
                    }
                    i += 1
                i = 0
                for fSubtitulo in soup.find_all(class_='c-headline__standfirst'):
                    # print(fSubtitulo.get_text().strip().removeprefix('O jornal Folha de S.Paulo é publicado pela Empresa Folha da Manhã S.A. CNPJ: 60.579.703/0001-48'))
                    if fSubtitulo.get_text().strip() != 'O jornal Folha de S.Paulo é publicado pela Empresa Folha da Manhã S.A. CNPJ: 60.579.703/0001-48':
                        dadosFolha[i]['dados']['subtitulo'] = fSubtitulo.get_text().strip()
                    i += 1    
                i = 0
                for fLink in soup.find_all(class_='c-headline__content'):
                    # print(gLink.find('a').get('href'))
                    dadosFolha[i]['dados']['Link'] = fLink.find('a').get('href')
                    i += 1
                ## Fim Folha
                ## Gazeta do Povo
                i = 0
                for gpTitulo in soup.find_all(class_='post-title'):
                    # print(gpTitulo.get_text().strip())
                    dadosGazeta[i] = {
                        'site': url,
                        'dados': {
                            'titulo': gpTitulo.get_text().strip()
                        }
                    }
                    i += 1
                i = 0
                for gpSubtitulo in soup.find_all(class_='post-summary'):
                    # print(gpSubtitulo.get_text().strip())
                    dadosGazeta[i]['dados']['subtitulo'] = gpSubtitulo.get_text().strip()
                    i += 1
                i = 0
                for gpLink in soup.find_all(class_='post-url'):
                    # print(gpLink.get('href'))
                    dadosGazeta[i]['dados']['Link'] = gpLink.get('href')
                    i += 1
                ## Fim Gazeta
                    
                ## Estadao
                i = 0
                for estadoTitulo in soup.find_all(class_='link-title'):
                    # print(estadoTitulo.find('h3').get_text().strip())
                    dadosEstadao[i] = {
                        'site': url,
                        'dados': {
                            'titulo': estadoTitulo.find('h3').get_text().strip(),
                            'Link': estadoTitulo.get('href')
                        }
                    }
                    i += 1
            try:
                dadosUol = {}
                dadosMetropoles = {}
                i = 0

                for url in searchEngineGoogle:
                    content = self.GetContentGoogleSearch(url)
                    jsonContent = json.loads(content['dados'])

                    if url == searchEngineGoogle[0]:
                        for uolTitle in jsonContent['results']:
                            dadosUol[i] = {
                                'site': url,
                                'dados': {
                                    'titulo': uolTitle['richSnippet']['metatags']['ogTitle'],
                                    'subtitulo': uolTitle['richSnippet']['metatags']['ogDescription'],
                                    'Link': uolTitle['url']
                                }
                            }
                            i += 1
                    if url == searchEngineGoogle[1]:
                        i = 0
                        for metrotitle in jsonContent['results']:
                            dadosMetropoles[i] = {
                                'site':url,
                                'dados': {
                                    'titulo': metrotitle['richSnippet']['metatags']['ogTitle'],
                                    'subtitulo':metrotitle['richSnippet']['metatags']['ogDescription'],
                                    'Link': metrotitle['url']
                                }
                            }
                            i += 1
                    
                    if dadosG1 != {} and dadosFolha != {} and dadosGazeta != {} and dadosEstadao != {} and dadosUol != {} and dadosMetropoles != {}: 
                        completeData = {
                            'Folha_de_sao_paulo':dadosFolha,
                            'G1': dadosG1,
                            'Gazeta_do_povo': dadosGazeta,
                            'Estadao': dadosEstadao,
                            'Metropoles': dadosMetropoles,
                            'UOL': dadosUol
                    }
            except Exception as e:
                print(e)
                print('aqui')
        except Exception as e:
            print(e)
        return completeData

    def GetSimilarity(self): ## Após "pegar" as informações de um conjunto de notícias, precisamos agora análisar cada titulo e subtitulo para ver qual notícia é mais adequada com o que o usuário pesquisou
        Similaridade = {}
        g1Similar = {}
        gazetaSimilar = {}
        metropolesSimilar = {}
        folhaSimilar = {}
        uolSimilar = {}
        estadaoSimilar = {}

        try:
            rsData = self.GetData()
            ## Inicio G1
            nlp = spacy.load('pt_core_news_lg') ## Para carregar o pacote que usaremos para analisar os titulos e as manchetes
            s1 = nlp(self.newstoSearch) ## Cria um objeto com as informações estruturais gramaticais e semânticas do texto

            i = 0
            for gTitulo in rsData['G1']:
                s2 = nlp(rsData['G1'][gTitulo]['dados']['titulo'])


                g1Similar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%", ## round(s1.similarity(s2)* 100, 2 ) -> em s1.similarity(s2). Estamos comparando o nível de similaridade com o que foi pesquisado - pelo usuario - e o titulo/subtitulo
                    'titulo': rsData['G1'][gTitulo]['dados']['titulo'],          ## Após isso, multiplicamos por 100 para transformar em porcentagem e o round é para pegar 2 números após a vírgula
                    'Link': rsData['G1'][gTitulo]['dados']['Link']
                }
                i += 1
                # print(f"g1 Titulo: {round(s1.similarity(s2)*100, 2)}%")

            i = 0
            for gSubtitulo in rsData['G1']:
                s2 = nlp(rsData['G1'][gSubtitulo]['dados']['subtitulo'])

                g1Similar[i]['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                g1Similar[i]['subtitulo'] = rsData['G1'][gSubtitulo]['dados']['subtitulo']
                # print(f"g1 Subtitulo: {round(s1.similarity(s2)* 100, 2)}")
                i += 1
            ## fim g1
            ## Inicio Folha
            i = 0
            for fTitulo in rsData['Folha_de_sao_paulo']:
                s2 = nlp(rsData['Folha_de_sao_paulo'][fTitulo]['dados']['titulo'])

                folhaSimilar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%",
                    'titulo': rsData['Folha_de_sao_paulo'][fTitulo]['dados']['titulo'],
                    'Link': rsData['Folha_de_sao_paulo'][fTitulo]['dados']['Link']
                }
                # print(f"folha titulo: {round(s1.similarity(s2)*100, 2)}")
                i += 1

            i=0
            for fSubtitulo in rsData['Folha_de_sao_paulo']:
                s2 = nlp(rsData['Folha_de_sao_paulo'][fSubtitulo]['dados']['subtitulo'])

                folhaSimilar[i]['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                folhaSimilar[i]['subtitulo'] = rsData['Folha_de_sao_paulo'][fSubtitulo]['dados']['subtitulo']
                # print(f"folha subtitulo: {round(s1.similarity(s2)*100, 2)}")
                i += 1

            ## Fim Folha
            ## Inicio Gazeta
            i = 0
            for gpTitulo in rsData['Gazeta_do_povo']:
                s2 = nlp(rsData['Gazeta_do_povo'][gpTitulo]['dados']['titulo'])

                gazetaSimilar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)* 100, 2)}%",
                    'titulo': rsData['Gazeta_do_povo'][gpTitulo]['dados']['titulo'],
                    'Link': rsData['Gazeta_do_povo'][gpTitulo]['dados']['Link']
                }
                # print(f"Gazeta Titulo: {round(s1.similarity(s2)*100, 2)}")
                i += 1
            
            i = 0
            for gpSubtitulo in rsData['Gazeta_do_povo']:
                s2 = nlp(rsData['Gazeta_do_povo'][gpSubtitulo]['dados']['subtitulo'])

                gazetaSimilar[i]['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)* 100, 2)}"
                gazetaSimilar[i]['subtitulo'] = rsData['Gazeta_do_povo'][gpSubtitulo]['dados']['subtitulo']
                # print(f"Gazeta subtitulo: {round(s1.similarity(s2)*100, 2)}")
                i += 1
            ## Fim Gazeta
            ## Inicio Metropoles
            i = 0
            for metroTitulo in rsData['Metropoles']:
                s2 = nlp(rsData['Metropoles'][metroTitulo]['dados']['titulo'])

                metropolesSimilar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%",
                    'titulo': rsData['Metropoles'][metroTitulo]['dados']['titulo'],
                    'Link': rsData['Metropoles'][metroTitulo]['dados']['Link']
                }
                i += 1
            i = 0
            for metroSubtitulo in rsData['Metropoles']:
                s2 = nlp(rsData['Metropoles'][metroSubtitulo]['dados']['subtitulo'])

                metropolesSimilar[i]['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)*100,2)}%"
                metropolesSimilar[i]['subtitulo'] = rsData['Metropoles'][metroSubtitulo]['dados']['subtitulo']
                i += 1

            ## Fim Metropoles
            ## Inicio UOL
            i = 0
            for uoltitulo in rsData['UOL']:
                s2 = nlp(rsData['UOL'][uoltitulo]['dados']['titulo'])

                uolSimilar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%",
                    'titulo': rsData['UOL'][uoltitulo]['dados']['titulo'],
                    'Link': rsData['UOL'][uoltitulo]['dados']['Link']
                }
                i += 1
            
            i = 0
            for uolsubtitulo in rsData['UOL']:
                s2 = nlp(rsData['UOL'][uolsubtitulo]['dados']['subtitulo'])

                uolSimilar[i]['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                uolSimilar[i]['subtitulo'] = rsData['UOL'][uolsubtitulo]['dados']['subtitulo']

                i += 1
            
            ## Fim Uol
            ## Inicio Estadao
            
            i = 0
            for estadaotitulo in rsData['Estadao']:
                s2 = nlp(rsData['Estadao'][estadaotitulo]['dados']['titulo'])

                estadaoSimilar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100,2)}%",
                    'titulo': rsData['Estadao'][estadaotitulo]['dados']['titulo'],
                    'Link':rsData['Estadao'][estadaotitulo]['dados']['Link']
                }   
                i += 1

            if gazetaSimilar != {} and folhaSimilar != {} and g1Similar != {} and metropolesSimilar != {} and uolSimilar != {} and estadaoSimilar != {}:
                Similaridade = {
                    'Folha_de_sao_paulo_similaridade': folhaSimilar.get(max(folhaSimilar, key=lambda k:folhaSimilar[k]['SimilaridadeTitulo'])), ## Essa função de max, analisa todo o ditc(hashmap) e nos tras o maior valor que aquele dict possui
                    'Gazeta_do_povo_similaridade': gazetaSimilar.get(max(gazetaSimilar, key=lambda k:gazetaSimilar[k]['SimilaridadeTitulo'])),
                    'G1_similaridade': g1Similar.get(max(g1Similar, key=lambda k:g1Similar[k]['SimilaridadeTitulo'])),
                    'Metropoles_similaridade': metropolesSimilar.get(max(metropolesSimilar, key=lambda k: metropolesSimilar[k]['SimilaridadeTitulo'])),
                    'UOL_similaridade': uolSimilar.get(max(uolSimilar, key=lambda k: uolSimilar[k]['SimilaridadeTitulo'])),
                    'Estadao_similaridade': estadaoSimilar.get(max(estadaoSimilar, key=lambda k: estadaoSimilar[k]['SimilaridadeTitulo']))
                }
                return Similaridade
        except Exception as e:
            print('achei?')
            print(e)
            return e
    
    def SentimentAnalisys(self): ## Aqui analisaremos a emoção de cada texto, onde utilizaremos Neutro, Positivo e Negativo para avaliar
        nltk.download('vader_lexicon')
        try:
            rq = self.GetCorpus()
            
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
            folhaCorpus = {}
            gazetaCorpus = {}
            g1Corpus = {}
            metropolesCorpus = {}
            uolCorpus = {}
            estadaoCorpus = {}

            req = self.GetSimilarity()
            urls = [ ## Links de cada notícia
                req['Folha_de_sao_paulo_similaridade']['Link'],
                req['Gazeta_do_povo_similaridade']['Link'],
                f"https:{req['G1_similaridade']['Link']}",
                req['Metropoles_similaridade']['Link'],
                req['Estadao_similaridade']['Link'],
                req['UOL_similaridade']['Link']
            ]
            for url in urls:
                reqCorpus = requests.get(url)
                print(f"status_code: {reqCorpus.status_code}")
                print(url)
                htmlcontent = reqCorpus.content

                soup = BeautifulSoup(htmlcontent, 'html.parser')

                ## Folha
                i = 0
                fullcorpus = ''
                if url == urls[0]:
                    for fbody in soup.find_all(class_='c-news__body'):
                        while(i < len(fbody.find_all('p'))):
                            # print(body.find_all('p')[i].get_text().strip())
                            fullcorpus += fbody.find_all('p')[i].get_text().strip()
                            i += 1
                    folhaCorpus = {
                        'Corpus': fullcorpus
                    }
                
                ## Gazeta
                i = 0
                fullcorpus = ''
                if url == urls[1]:
                    for gaBody in soup.find_all(class_='wrapper'):
                        # print(gaBody.find_all('p'))
                        while (i < len(gaBody.find_all('p'))):
                            fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                            i += 1
                    gazetaCorpus = {
                        'Corpus': fullcorpus
                    }

                ## G1
                i = 0
                fullcorpus = ''
                link = ''
                if url == urls[2]:
                    for originalLink in soup.find('script'):
                        link = originalLink.format().rsplit('window.location.replace("')[1].rsplit('");')[0]
                    reqCorpus = requests.get(link) ## -> Os links do G1 tem um problema para serem feitos requests, pois acaba dando erro e nesse erro está o link correto
                    print(f"g1 status_code: {reqCorpus.status_code}")
                    htmlcontent = reqCorpus.content
                    soup = BeautifulSoup(htmlcontent, 'html.parser')

                    for g1body in soup.find_all(class_='wall protected-content'):
                        # print(g1body.find_all('p'))
                        while (i < len(g1body.find_all('p'))):
                            fullcorpus += g1body.find_all('p')[i].get_text().strip()
                            i += 1
                    g1Corpus = {
                        'Corpus': fullcorpus
                    }
            
                ## Metropoles
                i = 0
                fullcorpus = ''
                if url == urls[3]:
                    for metroBody in soup.find_all(class_='ConteudoNoticiaWrapper__Artigo-sc-19fsm27-1 iRPifh'):
                        # print(metroBody.find_all('p'))
                        while (i < len(metroBody.find_all('p'))):
                            fullcorpus += metroBody.find_all('p')[i].get_text().strip()
                            i += 1
                    metropolesCorpus = {
                        'Corpus': fullcorpus
                    }
                
                ## Estadao
                    
                i = 0
                fullcorpus = ''
                if url == urls[4]:
                    for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                        while(i < len(estadobody.find_all('p'))):
                            fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                            i += 1
                    estadobody = {
                        'Corpus': fullcorpus
                    }

                ## Uol
                i = 0
                fullcorpus = ''
                if url == urls[5]:
                    for uolBody in soup.find_all(class_='content'): ## Situacao caso seja para a BAND
                        while (i < len(uolBody.find_all('p'))):
                            fullcorpus += uolBody.find_all('p')[i].get_text().strip()
                            i += 1
                    uolCorpus = {
                        'Corpus': fullcorpus
                    }
            return {'Folha_de_sao_paulo':folhaCorpus, 'Gazeta_do_povo':gazetaCorpus, 'G1': g1Corpus, 'Metropoles': metropolesCorpus, 'Estadao': estadobody, 'UOL':uolCorpus}, 200
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