# app/utils/geradores.py

"""
Arquivo de utilidades para geração de dados úteis para o projeto.
"""

import hashlib
import time


def gerar_id() -> str:
    """
    Gera um ID único para cada tag.
    """
    return hashlib.md5(str(time.time()).encode()).hexdigest()
