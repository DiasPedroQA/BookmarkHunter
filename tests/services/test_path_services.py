# pylint: disable=C, R, E, W


from _pytest.python_api import RaisesContext
import pytest
from app.services.path_services import (
    sanitizar_caminho,
    verificar_caminho_absoluto,
    verificar_caminho_relativo,
    extrair_pasta_principal,
    verificar_arquivo,
    validar_caminho,
)


# Testes para sanitizar_caminho
@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("/home/user/invalid&path", "/home/user/invalidpath"),
        ("C:\\Invalid?Path", "C:/InvalidPath"),
        ("./relative&path!", "./relativepath"),
        ("../relative<>path", "../relativepath"),
        ("/home/user/valid_path", "/home/user/valid_path"),
    ],
)
def test_sanitizar_caminho(caminho: str, expected: str):
    assert sanitizar_caminho(caminho) == expected


# Testes para verificar_caminho_absoluto
@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("/home/user/docs", True),
        ("C:\\Users\\user", False),
        ("./relative/path", False),
        ("../relative/path", False),
        ("relative/path", False),
    ],
)
def test_verificar_caminho_absoluto(caminho: str, expected: bool):
    assert verificar_caminho_absoluto(caminho) == expected


# Testes para verificar_caminho_relativo
@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("./relative/path", True),
        ("../relative/path", True),
        ("/home/user/docs", False),
        ("C:\\Users\\user", False),
        ("relative/path", False),
    ],
)
def test_verificar_caminho_relativo(caminho: str, expected: bool):
    assert verificar_caminho_relativo(caminho) == expected


# Testes para extrair_pasta_principal
@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("/home/user/folder/file.txt", "folder"),
        ("C:\\Users\\user\\folder\\file.txt", "folder"),
        ("/home/user/folder/", "user"),
        ("./relative/folder/file.txt", "folder"),
        ("../relative/folder/file.txt", "folder"),
        ("file.txt", None),
        ("/home/user/", "home"),
    ],
)
def test_extrair_pasta_principal(caminho: str, expected: None | str):
    assert extrair_pasta_principal(caminho) == expected


# Testes para verificar_arquivo
@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("/home/user/file.txt", True),
        ("C:\\Users\\user\\file.txt", True),
        ("./relative/file.txt", True),
        ("../relative/file.txt", True),
        ("/home/user/folder/", False),
        ("/home/user/folder", False),
        ("file", False),
    ],
)
def test_verificar_arquivo(caminho: str, expected: bool):
    assert verificar_arquivo(caminho) == expected


# Testes para exceções - Verificando as exceções que devem ser levantadas
@pytest.mark.parametrize(
    "function, caminho, expected_exception",
    [
        (sanitizar_caminho, None, ValueError),
        (sanitizar_caminho, "", ValueError),
        (verificar_caminho_absoluto, None, ValueError),
        (verificar_caminho_relativo, None, ValueError),
        (extrair_pasta_principal, None, ValueError),
        (verificar_arquivo, None, ValueError),
        (validar_caminho, None, ValueError),
        (validar_caminho, "", ValueError),
    ],
)
def test_funcoes_excecoes(function, caminho: None | str, expected_exception: type):
    with pytest.raises(expected_exception):
        function(caminho)


# Teste para a exceção KeyError, caso uma regex não seja encontrada
@pytest.mark.parametrize(
    "function, caminho, expected_exception",
    [
        (sanitizar_caminho, "/home/user/test", KeyError),
        (verificar_caminho_absoluto, "/home/user/test", KeyError),
        (verificar_caminho_relativo, "/home/user/test", KeyError),
        (extrair_pasta_principal, "/home/user/test", KeyError),
        (verificar_arquivo, "/home/user/test", KeyError),
    ],
)
def test_excecoes_regex_keyerror(function, caminho: str, expected_exception: type):
    with pytest.raises(expected_exception):
        function(caminho)
