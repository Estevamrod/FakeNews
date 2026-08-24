from dataclasses import dataclass
from typing import Optional

@dataclass
class Noticias:
  titulo: str
  subtitulo: str
  link: str
  fonte: str
  data_publicacao: Optional[str] = None
  conteudo: Optional[str] = None