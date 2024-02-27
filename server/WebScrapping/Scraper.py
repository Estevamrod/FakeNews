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
        urls = [ 
            'https://g1.globo.com/busca/?order=relevant&', 
            #G1
            'https://search.folha.uol.com.br/?site=todos&',
            # Folha de São Paulo
            'https://www.gazetadopovo.com.br/busca/?', ## Utiliza q
            # Gazeta do Povo
            'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=pt-PT&source=gcsc&gss=.com&cselibv=8435450f13508ca1&cx=004590593083191455447%3A5j_p3qfagic&safe=off&cse_tok=AB-tC_6pEVBRQzm5COyQ25W5ni_9%3A1709029191361&sort=&exp=cc%2Cdtsq-3&fexp=72497452&callback=google.search.cse.api2009&'
        ]
        try:
            dadosG1 = {}
            dadosFolha = {}
            dadosGazeta = {}
            dadosMetropoles = {}
            ComInfo = {}

            for url in urls:
                if url != urls[3]:    
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
                else:
                    try:
                        rq = requests.get(url, params={'q': self.newstoSearch.replace(" ", "+")})
                        print(f"status_code: {rq.status_code}")
                        htmlText = rq.text.split('/*O_o*/')[1].split('google.search.cse.api2009(')[1].split(');')[0]
                        jsonContent = json.loads(htmlText)

                        i = 0
                        for mainInfo in jsonContent['results']:
                            dadosMetropoles[i] = {
                                'site': url,
                                'dados': {
                                    'titulo': mainInfo['titleNoFormatting'].split(' ...')[0],
                                    'Link': mainInfo['url']
                                }
                            }
                            i += 1
                    except Exception as e:
                        print(e)
                
                if dadosG1 != {} and dadosFolha != {} and dadosGazeta != {} and dadosMetropoles:
                        ComInfo = {
                            'Folha_de_sao_paulo':dadosFolha,
                            'G1': dadosG1,
                            'Gazeta_do_povo': dadosGazeta,
                            'Metropoles': dadosMetropoles
                        }
                        return ComInfo
        except Exception as e:
            print(e)

    def GetSimilarity(self): ## Após "pegar" as informações de um conjunto de notícias, precisamos agora análisar cada titulo e subtitulo para ver qual notícia é mais adequada com o que o usuário pesquisou
        Similaridade = {}
        g1Similar = {}
        gazetaSimilar = {}
        metropolesSimilar = {}
        folhaSimilar = {}

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
                
                # print(folhaSimilar.get(max(folhaSimilar, key=lambda k:folhaSimilar[k]['SimilaridadeTitulo'])))
                # print(gazetaSimilar.get(max(gazetaSimilar, key=lambda k:gazetaSimilar[k]['SimilaridadeTitulo'])))
                # print(g1Similar.get(max(g1Similar, key=lambda k:g1Similar[k]['SimilaridadeTitulo'])))

            i = 0
            for metroTitulo in rsData['Metropoles']:
                s2 = nlp(rsData['Metropoles'][metroTitulo]['dados']['titulo'])

                metropolesSimilar[i] = {
                    'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%",
                    'titulo': rsData['Metropoles'][metroTitulo]['dados']['titulo'],
                    'Link': rsData['Metropoles'][metroTitulo]['dados']['Link']
                }
                i += 1


            if gazetaSimilar != {} and folhaSimilar != {} and g1Similar != {} and metropolesSimilar != {}:
                Similaridade = {
                    'Folha_de_sao_paulo_similaridade': folhaSimilar.get(max(folhaSimilar, key=lambda k:folhaSimilar[k]['SimilaridadeTitulo'])), ## Essa função de max, analisa todo o ditc(hashmap) e nos tras o maior valor que aquele dict possui
                    'Gazeta_do_povo_similaridade': gazetaSimilar.get(max(gazetaSimilar, key=lambda k:gazetaSimilar[k]['SimilaridadeTitulo'])),
                    'G1_similaridade': g1Similar.get(max(g1Similar, key=lambda k:g1Similar[k]['SimilaridadeTitulo'])),
                    'Metropoles_similaridade': metropolesSimilar.get(max(metropolesSimilar, key=lambda k: metropolesSimilar[k]['SimilaridadeTitulo']))
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

            print(f"Folha de Sao Paulo artigo: {folhaCorpusSentiment}")
            print(f"Gazeta do Povo artigo: {gazetaCorpusSentiment}")
            print(f"G1 artigo: {g1CorpusSentiment}")
            print(f"Metropoles artigo: {metropolesSentiment}")

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
                }
            }
        except Exception as e:
            print('aqui')
            print(e)
            return e
    
    def GetCorpus(self): ## Aqui pegamos o corpo da notícia que é mais adequada com o que se é pesquisado pelo usuário
        try:
            folhaCorpus = {}
            gazetaCorpus = {}
            g1Corpus = {}

            req = self.GetSimilarity()
            urls = [ ## Links de cada notícia
                req['Folha_de_sao_paulo_similaridade']['Link'],
                req['Gazeta_do_povo_similaridade']['Link'],
                f"https:{req['G1_similaridade']['Link']}",     
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
                # print(gazetaCorpus)
                
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
            
            return {'Folha_de_sao_paulo':folhaCorpus, 'Gazeta_do_povo':gazetaCorpus, 'G1': g1Corpus}, 200
        except Exception as e:
            print('ou sera aqui?')
            print(e)
            return e
