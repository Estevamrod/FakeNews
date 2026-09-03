from ..items import Noticias

class Limpeza:

    def DescarteNoticias(self, lista_noticias: list[Noticias]) -> list[Noticias]:
        manter = []
        visto = set()

        for noticia in lista_noticias:
            if not noticia.titulo or not noticia.link:
                continue

            if noticia.link in visto:
                continue

            visto.add(noticia.link)
            manter.append(noticia)

        return manter
