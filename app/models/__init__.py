# app/models/__init__.py

"""
Módulo de modelos.
Este módulo contém as classes de modelos para o aplicativo.

Classes:
    TagProcessor: Classe para processar tags HTML.
    Arquivo: Classe para representar um arquivo.
    Pasta: Classe para representar uma pasta.

Todos os modelos são importados neste módulo para facilitar o acesso.
"""

from .bookmark_model import TagProcessor
from .file_model import Arquivo
from .folder_model import Pasta

__all__ = ["TagProcessor", "Arquivo", "Pasta"]
