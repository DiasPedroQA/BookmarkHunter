# app/models/__init__.py

"""
Módulo de modelos.
Este módulo contém as classes de modelos para o aplicativo.

Classes:
    ObjetoTag: Classe para processar tags HTML.
    ObjetoArquivo: Classe para representar um arquivo.
    ObjetoPasta: Classe para representar uma pasta.

Todos os modelos são importados neste módulo para facilitar o acesso.
"""

from .bookmark_model import ObjetoTag
from .path_model import BasePathModel
# from .file_model import ObjetoArquivo
# from .folder_model import ObjetoPasta

__all__ = [
    "ObjetoTag",
    "BasePathModel",
    # "ObjetoArquivo",
    # "ObjetoPasta"
]
