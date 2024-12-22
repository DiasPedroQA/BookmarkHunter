# app/utils/__init__.py

"""
Módulo de modelos.
Este módulo contém as funcionalidades extras para o aplicativo.

Funções:
    gerar_id: Função para gerar um ID único.
    formatar_timestamp: Função para formatar um timestamp para o formato brasileiro.

Todos os modelos são importados neste módulo para facilitar o acesso.
"""

from .geradores import gerar_id
from .conversores import formatar_timestamp

__all__ = ["gerar_id", "formatar_timestamp"]
