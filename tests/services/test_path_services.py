# pylint: disable=C, R, E, W

import pytest
from app.services.path_services import (
    get_regex_pattern,
    obter_data_acesso,
    obter_data_criacao,
    obter_data_modificacao,
    validar_caminho,
    sanitizar_caminho,
    verificar_caminho_absoluto,
    verificar_caminho_relativo,
    extrair_pasta_principal,
    verificar_arquivo,
)


def test_get_regex_pattern():
    assert (
        get_regex_pattern("CAMINHO_ABSOLUTO")
        == r"^(?:[a-zA-Z]:\\|/home/[a-zA-Z0-9_-]+/)"
    )
    assert get_regex_pattern("CAMINHO_RELATIVO") == r"^(?:\.{1,2}/)"
    assert get_regex_pattern("NOME_ITEM") == r"\.[a-zA-Z0-9]+$"
    assert get_regex_pattern("SANITIZAR_CAMINHO") == r"[^a-zA-Z0-9\- _./\\:]"
    assert get_regex_pattern("EXTRAIR_PASTA") == r"([^/\\]+)/[^/\\]+/?$"
    assert get_regex_pattern("VALIDACAO_CAMINHO") == r"[\\/]+"
    with pytest.raises(KeyError):
        get_regex_pattern("INVALID_REGEX")


def test_validar_caminho():
    assert (
        validar_caminho(caminho="/home/user//documents//file.txt", separador="/")
        == "/home/user/documents/file.txt"
    )
    assert (
        validar_caminho(caminho="//home//user//Downloads", separador="/")
        == "/home/user/Downloads"
    )
    with pytest.raises(ValueError):
        validar_caminho("")
    with pytest.raises(ValueError):
        validar_caminho(None)


def test_sanitizar_caminho():
    assert (
        sanitizar_caminho("/home/user/documents/file?.txt")
        == "/home/user/documents/file.txt"
    )
    with pytest.raises(ValueError):
        sanitizar_caminho("")


def test_verificar_caminho_absoluto():
    assert verificar_caminho_absoluto("/home/user/documents/file.txt")
    assert not verificar_caminho_absoluto("../relative/path/file.txt")
    assert not verificar_caminho_absoluto("relative/path/file.txt")


def test_verificar_caminho_relativo():
    assert verificar_caminho_relativo("../relative/path/file.txt")
    assert verificar_caminho_relativo("./relative/path/file.txt")
    assert not verificar_caminho_relativo("/home/user/documents/file.txt")


def test_extrair_pasta_principal():
    assert extrair_pasta_principal("/home/user/documents/file.txt") == "documents"
    assert extrair_pasta_principal("/home//user//Downloads//file.txt") == "Downloads"
    assert extrair_pasta_principal("/file.txt") is None
    assert extrair_pasta_principal("file.txt") is None


def test_verificar_arquivo():
    assert verificar_arquivo("/home/user/documents/file.txt")
    assert not verificar_arquivo("/home/user/documents/folder/")
    # pylint: disable=C, R, E, W


def test_get_regex_pattern():
    assert (
        get_regex_pattern("CAMINHO_ABSOLUTO")
        == r"^(?:[a-zA-Z]:\\|/home/[a-zA-Z0-9_-]+/)"
    )
    assert get_regex_pattern("CAMINHO_RELATIVO") == r"^(?:\.{1,2}/)"
    assert get_regex_pattern("NOME_ITEM") == r"\.[a-zA-Z0-9]+$"
    assert get_regex_pattern("SANITIZAR_CAMINHO") == r"[^a-zA-Z0-9\- _./\\:]"
    assert get_regex_pattern("EXTRAIR_PASTA") == r"([^/\\]+)/[^/\\]+/?$"
    assert get_regex_pattern("VALIDACAO_CAMINHO") == r"[\\/]+"
    with pytest.raises(KeyError):
        get_regex_pattern("INVALID_REGEX")


def test_validar_caminho():
    assert (
        validar_caminho(caminho="/home/user//documents//file.txt", separador="/")
        == "/home/user/documents/file.txt"
    )
    assert (
        validar_caminho(caminho="//home//user//Downloads", separador="/")
        == "/home/user/Downloads"
    )
    with pytest.raises(ValueError):
        validar_caminho("")
    with pytest.raises(ValueError):
        validar_caminho(None)


def test_sanitizar_caminho():
    assert (
        sanitizar_caminho("/home/user/documents/file?.txt")
        == "/home/user/documents/file.txt"
    )
    with pytest.raises(ValueError):
        sanitizar_caminho("")


def test_verificar_caminho_absoluto():
    assert verificar_caminho_absoluto("/home/user/documents/file.txt")
    assert not verificar_caminho_absoluto("../relative/path/file.txt")
    assert not verificar_caminho_absoluto("relative/path/file.txt")


def test_verificar_caminho_relativo():
    assert verificar_caminho_relativo("../relative/path/file.txt")
    assert verificar_caminho_relativo("./relative/path/file.txt")
    assert not verificar_caminho_relativo("/home/user/documents/file.txt")


def test_extrair_pasta_principal():
    assert extrair_pasta_principal("/home/user/documents/file.txt") == "documents"
    assert extrair_pasta_principal("/home//user//Downloads//file.txt") == "Downloads"
    assert extrair_pasta_principal("/file.txt") is None
    assert extrair_pasta_principal("file.txt") is None


def test_verificar_arquivo():
    assert verificar_arquivo("/home/user/documents/file.txt")
    assert not verificar_arquivo("/home/user/documents/folder/")


def test_obter_data_criacao():
    assert obter_data_criacao(1737658061.00) == "23/12/2024 12:34:21"
    assert "Erro ao formatar data" in obter_data_criacao("invalid_timestamp")
    assert "Erro ao formatar data" in obter_data_criacao(-12345)


def test_obter_data_modificacao():
    assert obter_data_modificacao(1737658061.00) == "23/12/2024 12:34:21"
    assert "Erro ao formatar data" in obter_data_modificacao("invalid_timestamp")
    assert "Erro ao formatar data" in obter_data_modificacao(-12345)


def test_obter_data_acesso():
    assert obter_data_acesso(1737658061.00) == "23/12/2024 12:34:21"
    assert "Erro ao formatar data" in obter_data_acesso("invalid_timestamp")
    assert "Erro ao formatar data" in obter_data_acesso(-12345)
