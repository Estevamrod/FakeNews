from dataclasses import dataclass
from typing import Optional

@dataclass
class Noticias:
  titulo: str
  subtitulo: str
  link: list[str]
  fonte: str
  data_publicacao: Optional[str] = None