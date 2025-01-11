"""
Testes para as funções do módulo services.py
"""

from datetime import datetime, timezone, timedelta

import pytest
from app.services import (
    obter_dados_caminho,
    obter_tamanho_arquivo,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
    obter_permissoes_caminho,
    obter_id_unico,
)


def formatar_data(timestamp: int) -> str:
    """Formata um timestamp em uma string de data."""
    tz_brasil = timezone(timedelta(hours=-3))  # Horário de Brasília
    return datetime.fromtimestamp(timestamp, tz=tz_brasil).strftime(
        "%d/%m/%Y %H:%M:%S"
    )


@pytest.mark.parametrize(
    "caminho, esperado",
    [
        (
            "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
            {
                "pasta_pai": "home/pedro-pm-dias/Downloads/Chrome",
                "nome_arquivo": "favoritos_23_12_2024",
                "extensao_arquivo": "html",
            },
        ),
        (
            "/home/pedro-pm-dias/Downloads/Chrome/",
            {
                "pasta_pai": "home/pedro-pm-dias/Downloads",
                "nome_pasta": "Chrome",
            },
        ),
    ],
)
def test_obter_dados_caminho(caminho: str, esperado: dict[str, str]) -> None:
    """Testa a função obter_dados_caminho para arquivos e pastas."""
    resultado = obter_dados_caminho(caminho)
    for chave, valor in esperado.items():
        assert resultado[chave] == valor


@pytest.mark.parametrize(
    "tamanho, esperado",
    [
        (500, "500 bytes"),
        (2048, "2.00 KB"),
        (1048576, "1.00 MB"),
        (1073741824, "1.00 GB"),
    ],
)
def test_obter_tamanho_arquivo(tamanho: int, esperado: str) -> None:
    """Testa a função obter_tamanho_arquivo."""
    assert obter_tamanho_arquivo(tamanho) == esperado


@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, formatar_data(1736614800)),  # 01/01/2021 @ 12:00am (UTC)
        (1736615520, formatar_data(1736615520)),  # 11/01/2025 @ 12:00am (UTC)
    ],
)
def test_obter_data_criacao(timestamp: int, esperado: str) -> None:
    """Testa a função obter_data_criacao com formatação padronizada."""
    data_criacao = obter_data_criacao(timestamp)
    assert esperado in data_criacao


@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, "11/01/2025 14:00:00"),
        (1736615520, "11/01/2025 14:12:00"),
    ],
)
def test_obter_data_modificacao(timestamp: int, esperado: str) -> None:
    """Testa a função obter_data_modificacao com formatação padronizada."""
    data_modificacao = obter_data_modificacao(timestamp)
    assert esperado in data_modificacao


@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, formatar_data(1736614800)),
        (1736615520, formatar_data(1736615520)),
    ],
)
def test_obter_data_acesso(timestamp: int, esperado: str) -> None:
    """Testa a função obter_data_acesso com formatação padronizada."""
    data_acesso = obter_data_acesso(timestamp)
    assert esperado in data_acesso


@pytest.mark.parametrize(
    "permissoes, esperado",
    [
        (0o755, "?rwxr-xr-x"),  # Permissões comuns de diretório
        (0o644, "?rw-r--r--"),  # Permissões comuns de arquivo
        (0o777, "?rwxrwxrwx"),  # Permissões de acesso total
    ],
)
def test_obter_permissoes_caminho(permissoes: int, esperado: str) -> None:
    """Testa a função obter_permissoes_caminho com múltiplos casos."""
    assert obter_permissoes_caminho(permissoes) == esperado


@pytest.mark.parametrize(
    "identificador, esperado_tamanho",
    [
        (12345, 36),  # ID válido
    ],
)
def test_obter_id_unico(identificador: int, esperado_tamanho: int) -> None:
    """Testa a função obter_id_unico."""
    id_unico = obter_id_unico(identificador)
    assert isinstance(id_unico, str)
    assert len(id_unico) == esperado_tamanho

    with pytest.raises(ValueError):
        obter_id_unico(-1)
