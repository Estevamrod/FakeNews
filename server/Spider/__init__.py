from .estadao import SpiderEstadao
from .gazetaPovo import SpiderGazeta
from .folhaSaoPaulo import SpiderFolha
from .G1 import SpiderG1
from .Config.config_patterns import patterns
from ..Pipeline.limpeza import Limpeza


__all__ = ['SpiderEstadao', 'SpiderGazeta', 'SpiderFolha', 'SpiderG1', 'patterns', 'Limpeza']