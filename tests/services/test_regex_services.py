# pylint: disable=C, R, E, W
# sourcery skip: no-conditionals-in-tests

# from typing import Literal
from app.services.regex_services import (
    contar_diretorios,
    obter_data_acesso,
    obter_data_criacao,
    obter_data_modificacao,
    obter_id_unico,
    sanitizar_prefixo_caminho,
    validar_caminho,
    sanitizar_caminho,
    validar_tamanho_nome_caminho,
    verificar_caminho_absoluto,
    verificar_caminho_relativo,
    extrair_pasta_principal,
    verificar_arquivo,
)


def test_validar_caminho():
    assert validar_caminho("a//b\\c") == "a/b/c"
    assert validar_caminho("") == "O caminho '' deve ser uma string não vazia."
    assert validar_caminho(" a/b/c ", separador="//") == "a//b//c"


def test_sanitizar_caminho():
    assert sanitizar_caminho("a/b/?<>|c") == "a/b/c"
    assert sanitizar_caminho("  a \ b / c  ") == "a / b / c"


def test_verificar_caminho_absoluto():
    assert verificar_caminho_absoluto("/home/user/documents") is True
    assert verificar_caminho_absoluto("./docs/file") is False


def test_verificar_caminho_relativo():
    assert verificar_caminho_relativo("../folder/file") is True
    assert verificar_caminho_relativo("/root/folder/file") is False


def test_extrair_pasta_principal():
    assert extrair_pasta_principal("/home/user/file.txt") == "user"
    assert extrair_pasta_principal("file.txt") is None


def test_verificar_arquivo():
    assert verificar_arquivo("file.txt") is True
    assert verificar_arquivo("folder/file") is False


def test_obter_data_criacao():
    assert obter_data_criacao(1672531200.0) == "31/12/2022 21:00:00"
    assert obter_data_criacao(None) == "31/12/1969 21:00:00"
    assert (
        obter_data_criacao("")
        == "O timestamp '' deve ser um número inteiro ou decimal."
    )


def test_obter_data_modificacao():
    assert obter_data_modificacao(1672531200.0) == "31/12/2022 21:00:00"
    assert obter_data_modificacao(None) == "31/12/1969 21:00:00"
    assert (
        obter_data_modificacao("")
        == "O timestamp '' deve ser um número inteiro ou decimal."
    )


def test_obter_data_acesso():
    assert obter_data_acesso(1672531200.0) == "31/12/2022 21:00:00"
    assert obter_data_acesso(None) == "31/12/1969 21:00:00"
    assert (
        obter_data_acesso("") == "O timestamp '' deve ser um número inteiro ou decimal."
    )


def test_obter_id_unico():
    assert len(obter_id_unico(10)) == 36
    assert obter_id_unico(0) == "O identificador deve ser um número inteiro positivo."
    assert obter_id_unico(-7) == "O identificador deve ser um número inteiro positivo."
    assert (obter_id_unico(123) == "37813542-0dca-5a8a-b2a2-b69c2d45583f")


def test_validar_tamanho_nome_caminho():
    assert validar_tamanho_nome_caminho("home/user/Downloads/Chrome/") is True
    assert validar_tamanho_nome_caminho("Downloads/Chrome/" * 260) == "O caminho excede o limite de 260 caracteres."


def test_contar_diretorios():
    assert contar_diretorios("home/user/Downloads/Chrome/") == 3
    assert contar_diretorios("../../Downloads/Chrome") == 2


def test_sanitizar_prefixo_caminho():
    assert sanitizar_prefixo_caminho("/home/user/Downloads/Chrome/") == "home/user/Downloads/Chrome"
    assert sanitizar_prefixo_caminho("../../Downloads/Chrome/") == "Downloads/Chrome"
