import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from .Scraper import Scraper
import logging

class Analysis: 
    tosearch:str
    
    def __init__(self, tosearch:str):
        self.newstoSearch = tosearch
        self.similarity_response = {}
    
    def Similarity(self): ## Após "pegar" as informações de um conjunto de notícias, precisamos agora análisar cada titulo e subtitulo para ver qual notícia é mais adequada com o que o usuário pesquisou
        similaridade = []
        rate = []
        most_rated = {}

        try:
            response = Scraper.GetData(self.newstoSearch)

            ## Inicio G1

            nlp = spacy.load('pt_core_news_lg') ## Para carregar o pacote que usaremos para analisar os titulos e as manchetes
            s1 = nlp(self.newstoSearch) ## Cria um objeto com as informações estruturais gramaticais e semânticas do texto

            for gTitulo in response['g1']:
                s2 = nlp(gTitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': round(s1.similarity(s2)*100, 2), 'titulo_original': gTitulo['dados']['titulo'], 'link_noticia': gTitulo['dados']['link']}, 'site_name':'g1'})

            g1Similar = list(filter(lambda x: x['site_name'] == 'g1', similaridade))
            i = 0
            for gSubtitulo in response['g1']:
                s2 = nlp(gSubtitulo['dados']['subtitulo'])

                g1Similar[i]['similaridade']['subtitulo'] = round(s1.similarity(s2)*100, 2)
                g1Similar[i]['similaridade']['subtitulo_original'] = gSubtitulo['dados']['subtitulo']
                i += 1

            ## fim g1
            ## Inicio Folha
            
            for fTitulo in response['folha_de_saopaulo']:
                s2 = nlp(fTitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': round(s1.similarity(s2)*100, 2), 'titulo_original': fTitulo['dados']['titulo'], 'link_noticia': fTitulo['dados']['link']}, 'site_name':'folha_de_saopaulo'})

            folhaSimiliar = list(filter(lambda x: x['site_name'] == 'folha_de_saopaulo', similaridade))
            i=0
            for fSubtitulo in response['folha_de_saopaulo']:
                s2 = nlp(fSubtitulo['dados']['subtitulo'])

                folhaSimiliar[i]['similaridade']['subtitulo'] = round(s1.similarity(s2)*100, 2)
                folhaSimiliar[i]['similaridade']['subtitulo_original'] = fSubtitulo['dados']['subtitulo']
                i += 1

            ## Fim Folha
            ## Inicio Gazeta

            for gpTitulo in response['gazeta_do_povo']:
                s2 = nlp(gpTitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': round(s1.similarity(s2)*100, 2), 'titulo_original': gpTitulo['dados']['titulo'], 'link_noticia': gpTitulo['dados']['link']}, 'site_name':'gazeta_do_povo'})
            
            gazetaSimilar = list(filter(lambda x:x['site_name'] == 'gazeta_do_povo', similaridade))
            i = 0
            for gpSubtitulo in response['gazeta_do_povo']:
                s2 = nlp(gpSubtitulo['dados']['subtitulo'])

                gazetaSimilar[i]['similaridade']['subtitulo'] = round(s1.similarity(s2)* 100, 2)
                gazetaSimilar[i]['similaridade']['subtitulo_original'] = gpSubtitulo['dados']['subtitulo']
                i += 1

            ## Fim Gazeta
            ## Inicio Estadao
            
            for estadaotitulo in response['estadao']:
                s2 = nlp(estadaotitulo['dados']['titulo'])
                similaridade.append({'similaridade':{'titulo': round(s1.similarity(s2)*100, 2), 'titulo_original': estadaotitulo['dados']['titulo'], 'link_noticia': estadaotitulo['dados']['link']}, 'site_name':'estadao'})
            
            estadaoSimilar = list(filter(lambda x:x['site_name'] == 'estadao', similaridade))
            i = 0
            for estadaoSubtitulo in response['estadao']:
                s2 = nlp(estadaoSubtitulo['dados']['subtitulo'])
                estadaoSimilar[i]['similaridade']['subtitulo'] = round(s1.similarity(s2)*100, 2)
                estadaoSimilar[i]['similaridade']['subtitulo_original'] = estadaoSubtitulo['dados']['subtitulo']
                i+= 1

            ## Similarity simplification

            rate.append({  ## Pega a média entre as porcentagens para gerar apenas um valor de similaridade entre as duas notícias de cada site
                'folha_de_saopaulo':{
                    'titulo': round((max(folhaSimiliar, key=lambda x: x['similaridade']['titulo'])['similaridade']['titulo'] + max(folhaSimiliar, key=lambda x: x['similaridade']['titulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'folha_de_saopaulo', similaridade)) != [] else 0,
                    'subtitulo': round((max(folhaSimiliar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['titulo'] + max(folhaSimiliar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'folha_de_saopaulo', similaridade)) != [] else 0,
                },
                'gazeta_do_povo':{
                    'titulo': round((max(gazetaSimilar, key=lambda x: x['similaridade']['titulo'])['similaridade']['titulo'] + max(gazetaSimilar, key=lambda x: x['similaridade']['titulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'gazeta_do_povo', similaridade)) != [] else 0,
                    'subtitulo': round((max(gazetaSimilar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['titulo'] + max(gazetaSimilar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'gazeta_do_povo', similaridade)) != [] else 0,
                },
                'g1':{
                    'titulo': round((max(g1Similar, key=lambda x: x['similaridade']['titulo'])['similaridade']['titulo'] + max(g1Similar, key=lambda x: x['similaridade']['titulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'g1', similaridade)) != [] else 0,
                    'subtitulo': round((max(g1Similar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['titulo'] + max(g1Similar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'g1', similaridade)) != [] else 0,
                },
                'estadao':{
                    'titulo': round((max(estadaoSimilar, key=lambda x: x['similaridade']['titulo'])['similaridade']['titulo'] + max(estadaoSimilar, key=lambda x: x['similaridade']['titulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'estadao', similaridade)) != [] else 0,
                    'subtitulo': round((max(estadaoSimilar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['titulo'] + max(estadaoSimilar, key=lambda x: x['similaridade']['subtitulo'])['similaridade']['subtitulo'])/2,2) if list(filter(lambda x:x['site_name'] == 'estadao', similaridade)) != [] else 0,
                }
            })

            ## Faz o processo de saber qual é mais parecido e salva os dados
            print(rate)
            for i in rate:
                if i['folha_de_saopaulo']:
                    folha_rated = max(i['folha_de_saopaulo']['titulo'], i['folha_de_saopaulo']['subtitulo']) if i['folha_de_saopaulo']['titulo'] != 0 and i['folha_de_saopaulo']['subtitulo'] != 0 else 0
                    most_rated['folha_de_saopaulo']= {
                        'highest_tax': folha_rated,
                        'base_on_what': ('titulo' if i['folha_de_saopaulo']['titulo'] == folha_rated else 'subtitulo') if folha_rated != 0 else [],
                        'data': (max(folhaSimiliar, key=lambda x:x['similaridade']['titulo'])['similaridade'] if i['folha_de_saopaulo']['titulo'] == folha_rated else max(folhaSimiliar, key=lambda x:x['similaridade']['titulo'])['similaridade']) if folha_rated != 0 else [],
                        'site_name':'folha_de_saopaulo'
                    }

                if i['gazeta_do_povo']:
                    gazeta_rated = max(i['gazeta_do_povo']['titulo'], i['gazeta_do_povo']['subtitulo']) if i['gazeta_do_povo']['titulo'] != 0 and i['gazeta_do_povo']['subtitulo'] != 0 else 0
                    most_rated['gazeta_do_povo'] = {
                        'highest_tax': gazeta_rated,
                        'base_on_what': ('titulo' if i['gazeta_do_povo']['titulo'] == gazeta_rated else 'subtitulo') if gazeta_rated != 0 else [],
                        'data': (max(gazetaSimilar, key=lambda x:x['similaridade']['titulo'])['similaridade'] if i['gazeta_do_povo']['titulo'] == gazeta_rated else max(gazetaSimilar, key=lambda x:x['similaridade']['titulo'])['similaridade']) if gazeta_rated != 0 else [],
                        'site_name':'gazeta_do_povo'
                    }

                if i['g1']:
                    g1_rated = max(i['g1']['titulo'], i['g1']['subtitulo']) if i['g1']['titulo'] != 0 and i['g1']['subtitulo'] != 0 else 0
                    most_rated['g1'] = {
                        'highest_tax': g1_rated,
                        'base_on_what': ('titulo' if i['g1']['titulo'] == g1_rated else 'subtitulo') if g1_rated != 0 else [],
                        'data': (max(g1Similar, key=lambda x:x['similaridade']['titulo'])['similaridade'] if i['g1']['titulo'] == g1_rated else max(g1Similar, key=lambda x:x['similaridade']['subtitulo'])['similaridade']) if g1_rated != 0 else [],
                        'site_name':'g1'
                    }

                if i['estadao']:
                    estadao_rated = max(i['estadao']['titulo'], i['estadao']['subtitulo']) if i['estadao']['titulo'] != 0 and i['estadao']['subtitulo'] != 0 else 0
                    most_rated['estadao'] = {
                        'highest_tax': estadao_rated,
                        'base_on_what': ('titulo' if i['estadao']['titulo'] == estadao_rated else 'subtitulo') if estadao_rated != 0 else [],
                        'data': (max(estadaoSimilar, key=lambda x:x['similaridade']['titulo'])['similaridade'] if i['estadao']['titulo'] == estadao_rated else max(estadaoSimilar, key=lambda x:x['similaridade']['subtitulo'])['similaridade']) if estadao_rated != 0 else [],
                        'site_name':'estadao'
                    }
                    
            self.similarity_response = most_rated
            return most_rated
        except:
            logging.exception('error')
            return {'msg':'Houve um erro ao tentar finalizar a solicitacao! Por favor tente novamente!', 'function':'GetSimilarity'},201

    def SentimentAnalisys(self): ## Aqui analisaremos a emoção de cada texto, onde utilizaremos Neutro, Positivo e Negativo para avaliar
        nltk.download('vader_lexicon')
        try:
            response = Scraper.GetCorpus(self.similarity_response)
            if response == []:
                return []

            sentiment = []
            for i in response:

                ## Folha de Sao Paulo
                if i == 'folha_de_saopaulo' and response[i] != []:
                    sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(response[i]), 'origin':'folha_de_saopaulo'})

                ## Gazeta do Povo
                if i == 'gazeta_do_povo' and response[i] != []:
                    sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(response[i]), 'origin':'gazeta_do_povo'})

                ## G1
                if i == 'g1' and response[i] != []:
                    sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(response[i]), 'origin':'g1'})

                ## Estadao
                if i == 'estadao' and response[i] != []:
                    sentiment.append({'title':SentimentIntensityAnalyzer().polarity_scores(response[i]), 'origin':'estadao'})

            return {
                'folha_de_saopaulo':{
                    # 'negativo': f"{round(folhaCorpusSentiment['neg']*100,2)}%",
                    'negativo': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['title']['neg']*100,2) if list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment)) != [] else []}%",
                    'neutro': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['title']['neu']*100,2) if list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment)) != [] else []}%",
                    'positivo': f"{round(list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment))[0]['title']['pos']*100,2) if list(filter(lambda x:x['origin'] == 'folha_de_saopaulo', sentiment)) != [] else []}%",
                },
                'gazeta_do_povo':{
                    'negativo': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['title']['neg']*100,2) if list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment)) != [] else []}%",
                    'neutro': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['title']['neu']*100,2) if list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment)) != [] else []}%",
                    'positivo': f"{round(list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment))[0]['title']['pos']*100,2) if list(filter(lambda x:x['origin'] == 'gazeta_do_povo', sentiment)) != [] else []}%",
                },
                'g1': {
                    'negativo': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['title']['neg']*100,2) if list(filter(lambda x:x['origin'] == 'g1', sentiment)) != [] else []}%",
                    'neutro': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['title']['neu']*100,2) if list(filter(lambda x:x['origin'] == 'g1', sentiment)) != [] else []}%",
                    'positivo': f"{round(list(filter(lambda x:x['origin'] == 'g1', sentiment))[0]['title']['pos']*100,2) if list(filter(lambda x:x['origin'] == 'g1', sentiment)) != [] else []}%",
                },
                'estadao': {
                    'negativo': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['title']['neg']*100,2) if list(filter(lambda x:x['origin'] == 'estadao', sentiment)) != [] else []}%",
                    'neutro': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['title']['neu']*100,2) if list(filter(lambda x:x['origin'] == 'estadao', sentiment)) != [] else []}%",
                    'positivo': f"{round(list(filter(lambda x:x['origin'] == 'estadao', sentiment))[0]['title']['pos']*100,2) if list(filter(lambda x:x['origin'] == 'estadao', sentiment)) != [] else []}%",
                }
            }
        except Exception as e:
            logging.exception('error')
        except:
            return {'msg':'Houve um erro ao tentar finalizar a solicitacao! Por favor tente novamente!', 'function':'sentiment'},201
    