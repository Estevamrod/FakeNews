from ..items import Noticias

class Limpeza:
    def __init__(self):
        pass

    def DescarteNoticias(self, lista_noticias: list[Noticias]) -> list[Noticias]:
        manter = []
        visto = set()

        for noticia in lista_noticias:
            print(noticia)
            if not noticia.titulo or not noticia.link:
                continue

            if noticia.link[0] in visto:
                continue

            visto.add(noticia.link[0])
            manter.append(noticia)

        return manter
