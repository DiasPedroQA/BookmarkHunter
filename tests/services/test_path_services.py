# pylint: disable=C, R, E, W


import re
from _pytest.python_api import RaisesContext
import pytest
from app.services.path_services import REGEX_UTEIS, validar_caminho


@pytest.mark.parametrize(
    "regex_key, test_string, expected",
    [
        ("CAMINHO_ABSOLUTO", "/home/user/", True),
        ("CAMINHO_ABSOLUTO", "C:\\Users\\user\\", True),
        ("CAMINHO_ABSOLUTO", "./relative/path", False),
        ("CAMINHO_RELATIVO", "./relative/path", True),
        ("CAMINHO_RELATIVO", "../relative/path", True),
        ("CAMINHO_RELATIVO", "/absolute/path", False),
        ("NOME_ITEM", "file.txt", True),
        ("NOME_ITEM", "file", False),
        ("SANITIZAR_CAMINHO", "valid_path-123", False),
        ("SANITIZAR_CAMINHO", "invalid_path?*<>", True),
        ("EXTRAIR_PASTA", "/home/user/folder/file.txt", True),
        ("EXTRAIR_PASTA", "file.txt", False),
    ],
)
def test_regex_patterns(regex_key: str, test_string: str, expected: bool):
    pattern = re.compile(REGEX_UTEIS[regex_key])
    match = bool(pattern.search(test_string))
    assert match == expected


@pytest.mark.parametrize(
    "caminho, expected",
    [
        ("/home/user/docs", "/home/user/docs"),
        ("/home//user///docs", "/home/user/docs"),
        ("C:\\Users\\user\\", "C:/Users/user"),
        ("./relative/path", "./relative/path"),
        ("../relative/path", "../relative/path"),
        ("", pytest.raises(ValueError)),
        (None, pytest.raises(ValueError)),
        (123, pytest.raises(ValueError)),
        ("path//with//multiple//slashes", "path/with/multiple/slashes"),
        ("   /home/user/docs/  ", "/home/user/docs"),
        ("   ////   ", "/"),
        ("/home/user/!@#$%^&*()_+", "/home/user/!@#$%^&*()_+"),
        (" /home///user/ /docs//  ", "/home/user/docs"),
    ],
)
def test_validar_caminho(
    caminho: None | str | int, expected: RaisesContext[ValueError] | str
):
    if isinstance(expected, str) and issubclass(expected, Exception):
        with expected:
            validar_caminho(caminho)
    else:
        assert validar_caminho(caminho) == expected
