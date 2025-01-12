# pylint: disable=E0611

"""
Testes para as funções do módulo services.py.
"""

from datetime import datetime, timezone, timedelta
import pytest
from app.services.file_services import obter_tamanho_arquivo
from app.services.path_services import (
    obter_dados_caminho,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
    obter_permissoes_caminho,
    obter_id_unico,
    sanitizar_caminho_relativo,
    _fatiar_caminho,
    _formatar_data,
)


def formatar_data(timestamp: int) -> str:
    """
    Formata um timestamp em uma string de data no horário de Brasília.

    Args:
        timestamp (int): O timestamp Unix.

    Returns:
        str: Data formatada no padrão "dd/mm/yyyy hh:mm:ss".
    """
    tz_brasil: timezone = timezone(timedelta(hours=-3))
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
            "/pasta/file.txt",
            {
                "pasta_pai": "pasta",
                "nome_arquivo": "file",
                "extensao_arquivo": "txt",
            },
        ),
        (
            "",
            {
                "pasta_pai": "",
            },
        ),  # Caminho vazio deve retornar {}
        (None, ValueError),  # Tipo inválido
    ],
)
def test_obter_dados_caminho(caminho: str, esperado: dict[str, str]) -> None:
    """Testa a função obter_dados_caminho para arquivos e pastas."""
    if isinstance(esperado, dict):
        resultado: dict[str, str] = obter_dados_caminho(caminho)
        assert resultado == esperado
    else:
        with pytest.raises(esperado):
            obter_dados_caminho(caminho)


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
        ("/../home/./user/", ["home", ".", "user"]),
        ("", []),  # Caminho vazio
        (123, ValueError),  # Tipo inválido
    ],
)
def test_fatiar_caminho(caminho: str, esperado: list[str]) -> None:
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
        (None, "Erro ao formatar a data"),  # Tipo inválido
        ("invalid", "Erro ao formatar a data"),  # Tipo inválido
    ],
)
def test_formatar_data(timestamp: int, esperado: str) -> None:
    """Testa a função _formatar_data."""
    if "Erro" in esperado:
        assert esperado in _formatar_data(timestamp)
    else:
        assert _formatar_data(timestamp) == esperado


# Testes para obter_data_criacao, obter_data_modificacao e obter_data_acesso
@pytest.mark.parametrize(
    "funcao, timestamp, esperado",
    [
        (obter_data_criacao, 1736614800, formatar_data(1736614800)),
        (obter_data_modificacao, 1736614800, formatar_data(1736614800)),
        (obter_data_acesso, 1736614800, formatar_data(1736614800)),
    ],
)
def test_datas(funcao, timestamp: int, esperado: str) -> None:
    """Testa as funções de obtenção de datas."""
    assert funcao(timestamp) == esperado


# Testes para obter_permissoes_caminho
@pytest.mark.parametrize(
    "caminho, esperado",
    [
        ("/tmp", {"leitura": True, "escrita": True, "execucao": True}),
        ("/root", {"leitura": False, "escrita": False, "execucao": False}),
        ("/path/inexistente", {"leitura": False, "escrita": False, "execucao": False}),
    ],
)
def test_obter_permissoes_caminho(caminho: str, esperado: dict[str, bool]) -> None:
    """Testa a função obter_permissoes_caminho."""
    resultado: dict[str, bool] = obter_permissoes_caminho(caminho)
    assert resultado == esperado


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
        id_unico: str = obter_id_unico(identificador)
        assert isinstance(id_unico, str)
        assert len(id_unico) == esperado_tamanho
    else:
        with pytest.raises(esperado_tamanho):
            obter_id_unico(identificador)


# Testes para sanitizar_caminho_relativo
@pytest.mark.parametrize(
    "caminho, esperado",
    [
        ("../relative/path", "relative/path"),
        ("/.././path/", "./path/"),
        ("", ""),  # Caminho vazio
    ],
)
def test_sanitizar_caminho_relativo(caminho: str, esperado: str) -> None:
    """Testa a função sanitizar_caminho_relativo."""
    assert sanitizar_caminho_relativo(caminho) == esperado
