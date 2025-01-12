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
    _fatiar_caminho,
    _formatar_data
)


def formatar_data(timestamp: int) -> str:
    """Formata um timestamp em uma string de data."""
    tz_brasil = timezone(timedelta(hours=-3))  # Horário de Brasília
    return datetime.fromtimestamp(timestamp, tz=tz_brasil).strftime("%d/%m/%Y %H:%M:%S")


# Testes para obter_dados_caminho
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
        (
            "file.txt",
            {
                "pasta_pai": "",
                "nome_arquivo": "file",
                "extensao_arquivo": "txt",
            },
        ),
        ("", {}),  # Caminho vazio
    ],
)
def test_obter_dados_caminho(caminho: str, esperado: dict[str, str]) -> None:
    """Testa a função obter_dados_caminho para arquivos e pastas."""
    resultado = obter_dados_caminho(caminho)
    for chave, valor in esperado.items():
        assert resultado.get(chave) == valor


# Testes para obter_tamanho_arquivo
@pytest.mark.parametrize(
    "tamanho, esperado",
    [
        (500, "500.00 Bytes"),
        (2048, "2.00 KB"),
        (1048576, "1.00 MB"),
        (1073741824, "1.00 GB"),
        (0, ValueError),  # Valor inválido
        (-1, ValueError),  # Valor negativo
    ],
)
def test_obter_tamanho_arquivo(tamanho: int, esperado: str) -> None:
    """Testa a função obter_tamanho_arquivo."""
    if isinstance(esperado, str):
        assert obter_tamanho_arquivo(tamanho) == esperado
    else:
        with pytest.raises(esperado):
            obter_tamanho_arquivo(tamanho)


# Testes para _fatiar_caminho
@pytest.mark.parametrize(
    "caminho, esperado",
    [
        ("/home/user/docs/", ["home", "user", "docs"]),
        ("/../home/./user/", ["home", "user"]),
        ("", []),  # Caminho vazio
        (123, ValueError),  # Tipo inválido
    ],
)
def test_fatiar_caminho(caminho, esperado):
    """Testa a função _fatiar_caminho com diversos casos."""
    if isinstance(esperado, list):
        assert _fatiar_caminho(caminho) == esperado
    else:
        with pytest.raises(esperado):
            _fatiar_caminho(caminho)


# Testes para _formatar_data
@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, "11/01/2025 14:00:00"),
        (None, "Tipo de dado inválido"),  # Tipo inválido
        ("invalid", "Tipo de dado inválido"),  # Tipo inválido
    ],
)
def test_formatar_data(timestamp, esperado):
    """Testa a função _formatar_data."""
    if "inválido" in esperado:
        assert esperado in _formatar_data(timestamp)
    else:
        assert _formatar_data(timestamp) == esperado


# Testes para obter_data_criacao
@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, formatar_data(1736614800)),
    ],
)
def test_obter_data_criacao(timestamp: int, esperado: str) -> None:
    """Testa a função obter_data_criacao."""
    assert obter_data_criacao(timestamp) == esperado


# Testes para obter_data_acesso
@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, formatar_data(1736614800)),
    ],
)
def test_obter_data_acesso(timestamp: int, esperado: str) -> None:
    """Testa a função obter_data_acesso."""
    assert obter_data_acesso(timestamp) == esperado


# Testes para obter_data_modificacao
@pytest.mark.parametrize(
    "timestamp, esperado",
    [
        (1736614800, formatar_data(1736614800)),
    ],
)
def test_obter_data_modificacao(timestamp: int, esperado: str) -> None:
    """Testa a função obter_data_modificacao."""
    assert obter_data_modificacao(timestamp) == esperado


# Testes para obter_permissoes_caminho
@pytest.mark.parametrize(
    "caminho, esperado",
    [
        ("/tmp", {"leitura": True, "escrita": True, "execucao": True}),
        ("/root", {"leitura": False, "escrita": False, "execucao": False}),
        ("/path/inexistente", OSError),  # Caminho inválido
    ],
)
def test_obter_permissoes_caminho(caminho, esperado):
    """Testa a função obter_permissoes_caminho."""
    if isinstance(esperado, dict):
        resultado = obter_permissoes_caminho(caminho)
        assert resultado == esperado
    else:
        with pytest.raises(esperado):
            obter_permissoes_caminho(caminho)


# Testes para obter_id_unico
@pytest.mark.parametrize(
    "identificador, esperado_tamanho",
    [
        (12345, 36),  # ID válido
        (0, ValueError),  # Identificador inválido
        (-1, ValueError),  # Identificador negativo
    ],
)
def test_obter_id_unico(identificador: int, esperado_tamanho: int) -> None:
    """Testa a função obter_id_unico."""
    if isinstance(esperado_tamanho, int):
        id_unico = obter_id_unico(identificador)
        assert isinstance(id_unico, str)
        assert len(id_unico) == esperado_tamanho
    else:
        with pytest.raises(esperado_tamanho):
            obter_id_unico(identificador)
