# pylint: disable=C, R, E, W

"""
Módulo auxiliar para manipulação de caminhos e datas.

Funções disponíveis:
1. Manipulação de datas:
    - obter_data_criacao
    - obter_data_modificacao
    - obter_data_acesso
2. Manipulação de permissões e identificadores:
    - obter_permissoes_caminho
    - obter_id_unico
3. Manipulação de caminhos:
    - sanitizar_caminho
    - validar_tamanho_nome_caminho
    - verificar_caminho_absoluto
    - verificar_caminho_relativo
    - contar_diretorios
    - extrair_nome_item
    - extrair_pasta_principal
    - extrair_pasta_mae
    - verificar_arquivo
    - sanitizar_prefixo_caminho
"""

from datetime import datetime
import re
from typing import Dict, Optional
import uuid


def validar_caminho(caminho: str, separador: str = "/") -> str:
    """
    Valida e normaliza um caminho fornecido.
    """
    if not isinstance(caminho, str) or not caminho.strip():
        return str(f"O caminho '{caminho}' deve ser uma string não vazia.")

    caminho_normalizado = re.sub(r"[\\/]+", separador, caminho.strip())
    return caminho_normalizado.rstrip(separador)


def sanitizar_caminho(caminho: str) -> str:
    """
    Remove caracteres inválidos do caminho e normaliza-o.
    """
    caminho_normalizado = validar_caminho(caminho)
    return re.sub(r"[^a-zA-Z0-9\- _./\\:]", "", caminho_normalizado)


def verificar_caminho_absoluto(caminho: str) -> bool:
    """
    Verifica se o caminho fornecido é absoluto.
    """
    caminho_normalizado = validar_caminho(caminho)
    return bool(
        re.match(r"^(?:[a-zA-Z]:\\|/home/[a-zA-Z0-9_-]+/)", caminho_normalizado)
    )


def verificar_caminho_relativo(caminho: str) -> bool:
    """
    Verifica se o caminho fornecido é relativo.
    """
    caminho_normalizado = validar_caminho(caminho)
    return bool(re.match(r"^(?:\.{1,2}/)", caminho_normalizado))


def extrair_pasta_principal(caminho: str) -> Optional[str]:
    """
    Extrai a pasta principal do caminho fornecido.
    """
    caminho_normalizado = validar_caminho(caminho)
    match = re.search(r"([^/\\]+)/[^/\\]+/?$", caminho_normalizado)
    return match[1] if match else None


def verificar_arquivo(caminho: str) -> bool:
    """
    Verifica se o caminho representa um arquivo.
    """
    caminho_normalizado = validar_caminho(caminho)
    return bool(re.search(r"\.[a-zA-Z0-9]+$", caminho_normalizado))


def _formatar_data(timestamp: float) -> str:
    """
    Converte um timestamp em uma data legível no formato 'dd/mm/yyyy hh:mm:ss'.
    """
    if not isinstance(timestamp, (int, float)):
        return str(f"O timestamp '{timestamp}' deve ser um número inteiro ou decimal.")

    return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")


def obter_data_criacao(timestamp: float) -> str:
    """
    Retorna a data de criação formatada a partir de um timestamp.
    """
    if timestamp is None:
        timestamp = 0  # Epoch para lidar com valores None
    return _formatar_data(timestamp)


def obter_data_modificacao(timestamp: float) -> str:
    """
    Retorna a data de modificação formatada a partir de um timestamp.
    """
    if timestamp is None:
        timestamp = 0  # Epoch para lidar com valores None
    return _formatar_data(timestamp)


def obter_data_acesso(timestamp: float) -> str:
    """
    Retorna a data de acesso formatada a partir de um timestamp.
    """
    if timestamp is None:
        timestamp = 0  # Epoch para lidar com valores None
    return _formatar_data(timestamp)


# Funções para manipulação de identificadores
def obter_id_unico(identificador: int) -> str:
    """Gera um UUID baseado em um identificador numérico positivo."""
    if identificador <= 0:
        return "O identificador deve ser um número inteiro positivo."
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(identificador)))


def validar_tamanho_nome_caminho(caminho: str) -> bool:
    """Valida se o tamanho do caminho não excede o limite de 260 caracteres."""
    if len(caminho) > 260:
        return "O caminho excede o limite de 260 caracteres."
    return True


def contar_diretorios(caminho: str) -> int:
    """Conta o número de diretórios no caminho fornecido."""
    separador: str = "/"
    return caminho.count(separador) - 1


def sanitizar_prefixo_caminho(caminho: str) -> str:
    """Remove prefixos inválidos e normaliza caminhos relativos."""
    return caminho.strip("/\\.")
