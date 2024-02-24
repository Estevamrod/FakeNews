import requests
from bs4 import BeautifulSoup
import spacy

class Scraper:
    def __init__(self, newstoSearch):
        self.newstoSearch = newstoSearch

    def GetData(self):
        if self.newstoSearch == "":
            return {'msg': 'Você está fazendo uma requisição, mas não cumprindo com todos os requisitos!', 'finished': False, 'error': True}, 200
        urls = [ 
            'https://g1.globo.com/busca/?order=relevant&', 
            #G1
            'https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=pt-PT&source=gcsc&gss=.com&cselibv=8435450f13508ca1&cx=004590593083191455447%3A5j_p3qfagic&safe=off&cse_tok=AB-tC_4Do8DTVS9qknBk5blZHo4O%3A1708726140776&sort=&exp=cc%2Cdtsq-3&fexp=72497452&callback=google.search.cse.api5179&',
            # Metropoles
            'https://search.folha.uol.com.br/?site=todos&'
            # Folha de São Paulo
        ]
        try:
            dadosG1 = {}
            dadosFolha = {}
            ComInfo = {}
            for url in urls:
                rs = requests.get(url, params={'q':self.newstoSearch.replace(" ", "+")})
                print(f"status code: {rs.status_code}")
                htmlcontent = rs.content

                i = 0 
                if url != urls[1]:
                    print(f'Actual url in request: {url}')
                    soup = BeautifulSoup(htmlcontent, 'html.parser')
                    ##inicio g1
                    for titulo in soup.find_all(class_='widget--info__title product-color'):
                        # print(i.get_text())
                        dadosG1[i] = {
                            'site':url, 
                            'dados': {
                                'titulo': titulo.get_text().strip()
                            }
                            }
                        i += 1
                    i = 0
                    for subtitulo in soup.find_all(class_='widget--info__description'):
                        dadosG1[i]['dados']['subtitulo'] = subtitulo.get_text().strip()
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
                    
                    # print(dadosG1)
                    # print(dadosFolha)
                        
                    ## Fim Folha
                    if dadosG1 != {} and dadosFolha != {}:
                        ComInfo = {
                            'Folha_de_sao_paulo':dadosFolha,
                            'G1': dadosG1
                        }
                        return ComInfo
                    
                # else:
                #     try:
                #         json_str = rs.text.lstrip('/*O_o*/')
                #         data = json.loads(json_str)
                #         print(data['results'])
                        
                #     except Exception as e:
                #         print(e)
        except Exception as e:
            print('erro da qui')
            print(e)

    def GetSimilarity(self):
        Similaridade = {}
        g1Similar = {}
        folhaSimilar = {}

        try:
            rsData = self.GetData()
            ##primeiro o g1
            nlp = spacy.load('pt_core_news_lg') ## Para carregar o pacote que usaremos para analisar os titulos e as manchetes
            s1 = nlp(self.newstoSearch)## Tokenizamos o query do usuario

            i = 0
            for gTitulo in rsData['G1']:
                s2 = nlp(rsData['G1'][gTitulo]['dados']['titulo'])


                g1Similar[i] = {
                    'dados': {
                        'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%",
                        'titulo': s2
                    }
                }
                i += 1
                print(f"g1 Titulo: {round(s1.similarity(s2)*100, 2)}%")

            i = 0
            for gSubtitulo in rsData['G1']:
                s2 = nlp(rsData['G1'][gSubtitulo]['dados']['subtitulo'])

                g1Similar[i]['dados']['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                g1Similar[i]['dados']['subtitulo'] = s2
                print(f"g1 Subtitulo: {round(s1.similarity(s2)* 100, 2)}")
                i += 1
            ## fim g1
            i = 0
            for fTitulo in rsData['Folha_de_sao_paulo']:
                s2 = nlp(rsData['Folha_de_sao_paulo'][fTitulo]['dados']['titulo'])

                folhaSimilar[i] = {
                    'dados': {
                        'SimilaridadeTitulo': f"{round(s1.similarity(s2)*100, 2)}%",
                        'titulo': s2
                    }
                }
                print(f"folha titulo: {round(s1.similarity(s2)*100, 2)}")
                i += 1

            i=0
            for fSubtitulo in rsData['Folha_de_sao_paulo']:
                s2 = nlp(rsData['Folha_de_sao_paulo'][fSubtitulo]['dados']['subtitulo'])

                folhaSimilar[i]['dados']['SimilaridadeSubtitulo'] = f"{round(s1.similarity(s2)*100, 2)}%"
                folhaSimilar[i]['dados']['subtitulo'] = s2
                print(f"folha subtitulo: {round(s1.similarity(s2)*100, 2)}")
                i += 1
            
            print(f"{g1Similar.get(max(g1Similar, key=lambda k:g1Similar[k]['dados']['SimilaridadeTitulo']))}")
            print(f"Folha de Sao Paulo")
            print(f"{folhaSimilar.get(max(g1Similar, key=lambda k:g1Similar[k]['dados']['SimilaridadeTitulo']))}")

            print(f"G1")
            print(rsData['G1'])
            print(f"Folha de Sao Paulo")
            print(rsData['Folha_de_sao_paulo'])

            return 'ok'
        except Exception as e:
            print('achei?')
            print(e)
            return e