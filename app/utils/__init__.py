# app/utils/__init__.py

"""
Módulo de modelos.
Este módulo contém as funcionalidades extras para o aplicativo.

Funções:
    gerar_id: Função para gerar um ID único.
    formatar_timestamp_int_para_data_brasil: Função para formatar um timestamp para o formato brasileiro.

Todos os modelos são importados neste módulo para facilitar o acesso.
"""

from .conversores import ConversoresUtils
from .geradores import Geradores

__all__ = [
    "ConversoresUtils",
    "Geradores",
]
