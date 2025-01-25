# pylint: disable=C, R, E, W


import re
from _pytest.python_api import RaisesContext
import pytest
from app.services.path_services import REGEX_UTEIS, validar_caminho


# Teste de expressões regulares
@pytest.mark.parametrize(
    "regex_key, test_string, expected",
    [
        # Testes para caminhos absolutos
        ("CAMINHO_ABSOLUTO", "/home/user/", True),
        ("CAMINHO_ABSOLUTO", "C:\\Users\\user\\", True),
        ("CAMINHO_ABSOLUTO", "./relative/path", False),
        # Testes para caminhos relativos
        ("CAMINHO_RELATIVO", "./relative/path", True),
        ("CAMINHO_RELATIVO", "../relative/path", True),
        ("CAMINHO_RELATIVO", "/absolute/path", False),
        # Testes para nome de itens
        ("NOME_ITEM", "file.txt", True),
        ("NOME_ITEM", "file", False),
        # Testes para sanitização
        ("SANITIZAR_CAMINHO", "valid_path-123", False),
        ("SANITIZAR_CAMINHO", "invalid_path?*<>", True),
        # Testes para extração de pastas
        ("EXTRAIR_PASTA", "/home/user/folder/file.txt", True),
        ("EXTRAIR_PASTA", "file.txt", False),
    ],
)
def test_regex_patterns(regex_key: str, test_string: str, expected: bool):
    pattern = re.compile(REGEX_UTEIS[regex_key])
    match = bool(pattern.search(test_string))
    assert match == expected


# Testes para validar_caminho
@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("path//with//multiple//slashes", "path/with/multiple/slashes"),
        ("/home/user/docs", "/home/user/docs"),
        ("/home//user///docs", "/home/user/docs"),
        ("C:\\Users\\user\\", "C:/Users/user"),
        ("./relative/path", "./relative/path"),
        ("../relative/path", "../relative/path"),
        ("   /home/user/docs/  ", "/home/user/docs"),
        ("   ////   ", "/"),
        ("/home/user/!@#$%^&*()_+", "/home/user/!@#$%^&*()_+"),
        (" /home///user/ /docs//  ", "/home/user/docs"),
        ("/home/user/!@#$%^&*()_+", "/home/user/!@#$%^&*()_+"),
        (" /home///user/ /docs//  ", "/home/user/docs"),
    ],
)
def test_validar_caminho_success(caminho, expected):
    assert validar_caminho(caminho) == expected

@pytest.mark.parametrize(
    "caminho, expected_exception",
    [
        (None, pytest.raises(ValueError)),
        ("", pytest.raises(ValueError)),
        (123, pytest.raises(ValueError)),
    ],
)
def test_validar_caminho_failure(caminho, expected_exception):
    with expected_exception:
        validar_caminho(caminho)
