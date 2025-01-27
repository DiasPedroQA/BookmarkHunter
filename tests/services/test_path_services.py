# pylint: disable=C0114, C0116


import pytest
from app.services.path_services import RegexPathAnalyzer


def test_sanitizar_caminho():
    assert (
        RegexPathAnalyzer.validar_e_sanitizar_caminho("/home/user/docs/")
        == "/home/user/docs/"
    )
    assert (
        RegexPathAnalyzer.validar_e_sanitizar_caminho("/home/user/docs/<>")
        == "/home/user/docs/"
    )
    assert (
        RegexPathAnalyzer.validar_e_sanitizar_caminho("C:\\User\\docs\\<>")
        == "C:/User/docs/"
    )
    assert (
        RegexPathAnalyzer.validar_e_sanitizar_caminho("C:\\User\\docs\\")
        == "C:/User/docs/"
    )
    assert (
        RegexPathAnalyzer.validar_e_sanitizar_caminho("/home/user/docs/")
        == "/home/user/docs/"
    )
    with pytest.raises(ValueError):
        RegexPathAnalyzer.validar_e_sanitizar_caminho("")
    with pytest.raises(ValueError):
        RegexPathAnalyzer.validar_e_sanitizar_caminho(" " * 261)


@pytest.mark.parametrize(
    "input_path, expected_result",
    [
        (
            "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
            {"absoluto": True, "relativo": False, "arquivo": True, "pasta": False},
        ),
        (
            "../../Downloads/Chrome/favoritos_23_12_2024.html",
            {"absoluto": False, "relativo": True, "arquivo": True, "pasta": False},
        ),
        (
            "/home/pedro-pm-dias/Downloads/Chrome/arquivo?*<>.html",
            {"absoluto": True, "relativo": False, "arquivo": True, "pasta": False},
        ),
        (
            "../Downloads/Chrome/imagens/arquivo?*<>.jpg",
            {"absoluto": False, "relativo": True, "arquivo": True, "pasta": False},
        ),
        (
            "/home/pedro-pm-dias/Downloads/Chrome/",
            {"absoluto": True, "relativo": False, "arquivo": False, "pasta": True},
        ),
        (
            "../../Downloads/Chrome/",
            {"absoluto": False, "relativo": True, "arquivo": False, "pasta": True},
        ),
        (
            "/home/pedro-pm-dias/Downloads/Chrome",
            {"absoluto": True, "relativo": False, "arquivo": False, "pasta": True},
        ),
        (
            "../../Downloads/Chrome/<>/",
            {"absoluto": False, "relativo": True, "arquivo": False, "pasta": True},
        ),
        (
            "file.txt",
            {"absoluto": False, "relativo": False, "arquivo": True, "pasta": False},
        ),
        (
            "/home/user/docs/file.txt",
            {"absoluto": True, "relativo": False, "arquivo": True, "pasta": False},
        ),
    ],
)
def test_verificar_tipo_caminho(input_path: str, expected_result: dict[str, bool]):
    result = RegexPathAnalyzer.verificar_tipo_caminho(input_path)
    assert result == expected_result


def test_extrair_pasta_principal():
    assert (
        RegexPathAnalyzer.extrair_pasta_principal("/home/user/docs/file.txt") == "docs"
    )
    assert RegexPathAnalyzer.extrair_pasta_principal("/home/user/docs/") == "user"
    assert RegexPathAnalyzer.extrair_pasta_principal("/home/user/") == "home"
    assert RegexPathAnalyzer.extrair_pasta_principal("/home/") is None
    assert RegexPathAnalyzer.extrair_pasta_principal("/") is None


def test_contar_diretorios():
    assert RegexPathAnalyzer.contar_diretorios("/home/user/docs/file.txt") == 3
    assert RegexPathAnalyzer.contar_diretorios("/home/user/docs/") == 3
    assert RegexPathAnalyzer.contar_diretorios("/home/user/") == 2
    assert RegexPathAnalyzer.contar_diretorios("/home/") == 1
    assert RegexPathAnalyzer.contar_diretorios("/") == 0


def test_analisar_caminho():
    analisador = RegexPathAnalyzer("/home/user/docs/file.txt")
    resultado = analisador.analisar_caminho()
    assert resultado == {
        "caminho_original": "/home/user/docs/file.txt",
        "pasta_principal": "docs",
        "numero_diretorios": 3,
        "absoluto": True,
        "relativo": False,
        "arquivo": True,
        "pasta": False,
    }
    analisador = RegexPathAnalyzer("../../user/docs/")
    resultado = analisador.analisar_caminho()
    assert resultado == {
        "caminho_original": "../../user/docs/",
        "pasta_principal": "user",
        "numero_diretorios": 4,
        "absoluto": False,
        "relativo": True,
        "arquivo": False,
        "pasta": True,
    }
