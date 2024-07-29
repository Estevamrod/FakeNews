import grequests
from bs4 import BeautifulSoup
import logging

class Scraper:
    def GetData(newstoSearch):  ## Aqui a gente vai utilizar para "pegar" os titulos, manchetes e os links de cada noticia
        
        data = []
        searchEngineStandart = [ ## Sites que utilizam a mesma syntax para realizar pesquisas. Ou seja, utilizando *q=* significando query ou pesquisa traduzindo ao pe da letra
            'https://g1.globo.com/busca/?order=recent&species=notícias&', 
            #G1
            
            'https://search.folha.uol.com.br/?periodo=ano&site=todos&',
            # Folha de São Paulo

            'https://www.gazetadopovo.com.br/busca/?sort=newest&period=last-year&',
            # Gazeta do Povo

            'https://busca.estadao.com.br/?tipo_conteudo=Todos&quando=no-ultimo-ano&',
            # Estadao   
        ]

        try:

            req = [grequests.get(str(url) + 'q=' + newstoSearch.replace(" ", "+")) for url in searchEngineStandart]
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
                'folha_de_saopaulo':folha,
                'gazeta_do_povo':   gp,
                'g1':               g1,
                'estadao':          estadao,
            }
        except Exception as e:
            logging.exception('error')
        except:
            return {'msg':'Houve um erro ao tentar finalizar a solicitacao! Por favor tente novamente!', 'function':'GetData'},201

    def GetCorpus(data): ## Aqui pegamos o corpo da notícia que é mais adequada com o que se é pesquisado pelo usuário
        try:
            corpus = []
            url = []
        
            for site_origin in data:
                if data[site_origin]['data'] != []:
                    url.append({'site_origin':site_origin, 'link': data[site_origin]['data']['link_noticia']})

            ## Start first with title link's based

            req = [grequests.get(link['link']) for link in url]
            responses = grequests.map(req, size=4)

            for response in responses:
                print(f"title get_corpus: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')

                ## Folha

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'folha_de_saopaulo' for index in corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url]):
                    for fbody in soup.find_all(class_='c-news__body'):
                        while(i < len(fbody.find_all('p'))):
                            fullcorpus += fbody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus':fullcorpus, 'site_origin':'folha_de_saopaulo'})
                
                ## Gazeta

                i = 0
                fullcorpus = ''
                if (any([index['site_origin'] == 'gazeta_do_povo' for index in corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in url]):
                    for gaBody in soup.find_all(class_='wrapper'):
                        while (i < len(gaBody.find_all('p'))):
                            fullcorpus += gaBody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus': fullcorpus, 'site_origin':'gazeta_do_povo'})
                
                ## G1

                i = 0
                fullcorpus = ''
                g1link = []
                if (any([index['site_origin'] == 'g1' for index in corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'g1' for index in url]):
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
                if (any([index['site_origin'] == 'estadao' for index in corpus]) == False) and  any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in url]):
                    for estadobody in soup.find_all(class_='styles__ContentWrapperContainerStyled-sc-1ehbu6v-0'):
                        while(i < len(estadobody.find_all('p'))):
                            fullcorpus += estadobody.find_all('p')[i].get_text().strip()
                            i += 1
                    corpus.append({'corpus': fullcorpus,'site_origin':'estadao'})

            return {
                'folha_de_saopaulo':    list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo', corpus))[0]['corpus'] if  list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo', corpus)) != [] else [],
                'gazeta_do_povo':       list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo', corpus))[0]['corpus'] if  list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo', corpus)) != [] else [],
                'g1':                   list(filter(lambda x:x['site_origin'] == 'g1', corpus))[0]['corpus'] if  list(filter(lambda x:x['site_origin'] == 'g1', corpus)) != []  else [],
                'estadao':              list(filter(lambda x:x['site_origin'] == 'estadao', corpus))[0]['corpus'] if list(filter(lambda x:x['site_origin'] == 'estadao', corpus)) != []  else []
            }
        except Exception as e:
            logging.exception('erro')
        except:
            return {'msg':'Houve um erro ao tentar finalizar a solicitacao! Por favor tente novamente!', 'function':'GetCorpus'},201
    
    def Getdate(content):
        try:
            url = []
            date_corpus= []

            for index in content:
                if content[index]['data'] !=  []:
                    url.append({'link':content[index]['data']['link_noticia'], 'site_origin':index})

            req = [grequests.get(link['link']) for link in url]
            responses = grequests.map(req, size=4)

            for response in responses:
                print(f"title get_date: {response.status_code}")
                soup = BeautifulSoup(response.content, 'html.parser')

                #Folha de Sao Paulo
                if (any([index['site_origin'] == 'folha_de_saopaulo' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'folha_de_saopaulo' for index in url]):
                    for folha_date in soup.find(class_='c-more-options__published-date'):
                        if folha_date.get_text().strip().isalpha() == False:
                            date_corpus.append({'datetime':folha_date.get_text().strip(), 'site_origin':'folha_de_saopaulo','origin': response.url})

                #Gazeta do povo
                if (any([index['site_origin'] == 'gazeta_do_povo' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'gazeta_do_povo' for index in url]):
                    for gazeta_date in soup.find(class_='wgt-date'):
                        if gazeta_date.get_text().strip().isalpha() == False:
                            date_corpus.append({'datetime':gazeta_date.get_text().strip(), 'site_origin':'gazeta_do_povo', 'origin': response.url})
                
                #G1
                formatt_link = []
                if (any([index['site_origin'] == 'g1' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'g1' for index in url]):
                    for getscript in soup.find('script'):
                        if 'window.location.replace' in getscript:
                            formatt_link.append({'link':getscript.format().rsplit('window.location.replace("')[1].rsplit('");')[0]})
                            
                    g1format_rq = [grequests.get(link['link']) for link in formatt_link]
                    g1format_res = grequests.map(g1format_rq, size=1)
                    for g1response in g1format_res:
                        print(f"title get_date g1 : {g1response.status_code}")
                        soup = BeautifulSoup(g1response.content, 'html.parser')

                        for g1date in soup.find(class_='content-publication-data__updated'):
                            if g1date.find_next('time').get_text().strip().isalpha() == False:
                                date_corpus.append({'datetime':g1date.find_next('time').get_text().strip(), 'site_origin':'g1', 'origin': response.url})
                                break

                #Estadao
                if (any([index['site_origin'] == 'estadao' for index in date_corpus]) == False) and any([index['link'] == response.url and index['site_origin'] == 'estadao' for index in url]):
                    for estadao_date in soup.find(class_='principal-dates'):
                        if estadao_date.find_next('time').get_text().strip().isalpha() == False:
                            date_corpus.append({'datetime':estadao_date.find_next('time').get_text().strip(), 'site_origin':'estadao', 'origin': response.url})
                            break
            
            return {
                'folha_de_saopaulo':    list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo', date_corpus))[0] if list(filter(lambda x:x['site_origin'] == 'folha_de_saopaulo', date_corpus)) != [] else [],
                'gazeta_do_povo':       list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo', date_corpus))[0] if list(filter(lambda x:x['site_origin'] == 'gazeta_do_povo', date_corpus)) != [] else [],
                'g1':                   list(filter(lambda x:x['site_origin'] == 'g1', date_corpus))[0] if list(filter(lambda x:x['site_origin'] == 'g1', date_corpus)) != [] else [],
                'estadao':              list(filter(lambda x:x['site_origin'] == 'estadao', date_corpus))[0] if list(filter(lambda x:x['site_origin'] == 'estadao', date_corpus)) != [] else []
            }
        except Exception as e:
            logging.exception('error')
        except:
            return {'msg':'Houve um erro ao tentar finalizar a solicitacao! Por favor tente novamente!', 'function':'Getdate'},201

