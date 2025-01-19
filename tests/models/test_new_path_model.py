# pylint: disable=C, R, E, W

import pytest
from pathlib import Path
from app.models.new_path_model import AnalisadorCaminho, AnalisadorPathlib


@pytest.fixture
def caminho_absoluto() -> str:
    return "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"


@pytest.fixture
def caminho_relativo() -> str:
    return "../../Downloads/Chrome/favoritos_23_12_2024.html"


@pytest.fixture
def diretorio_referencia() -> str:
    return "/home/pedro-pm-dias/Downloads"


def test_caminho_eh_absoluto(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert analisador.caminho_eh_absoluto() is True

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_eh_absoluto() is False


def test_caminho_eh_relativo(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert analisador.caminho_eh_relativo() is False

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_eh_relativo() is True


def test_caminho_eh_caminho_valido(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert analisador.caminho_eh_caminho_valido() is True

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_eh_caminho_valido() is True

    analisador = AnalisadorCaminho("invalid|path")
    assert analisador.caminho_eh_caminho_valido() is False


def test_caminho_obter_nome_arquivo(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert analisador.caminho_obter_nome_arquivo() == "favoritos_23_12_2024.html"

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_obter_nome_arquivo() == "favoritos_23_12_2024.html"


def test_caminho_obter_diretorio(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert (
        analisador.caminho_obter_diretorio() == "/home/pedro-pm-dias/Downloads/Chrome"
    )

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_obter_diretorio() == "../../Downloads/Chrome"


def test_caminho_possui_extensao(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert analisador.caminho_possui_extensao(".html") is True
    assert analisador.caminho_possui_extensao(".txt") is False

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_possui_extensao(".html") is True
    assert analisador.caminho_possui_extensao(".txt") is False


def test_caminho_contar_segmentos(caminho_absoluto: str, caminho_relativo: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert analisador.caminho_contar_segmentos() == 5

    analisador = AnalisadorCaminho(caminho_relativo)
    assert analisador.caminho_contar_segmentos() == 5


def test_caminho_converter_para_relativo(caminho_absoluto: str, diretorio_referencia: str):
    analisador = AnalisadorCaminho(caminho_absoluto)
    assert (
        str(analisador.caminho_converter_para_relativo(diretorio_referencia))
        == "Chrome/favoritos_23_12_2024.html"
    )


def test_caminho_converter_para_absoluto(caminho_relativo, diretorio_referencia: str):
    analisador = AnalisadorCaminho(caminho_relativo)
    assert (
        analisador.caminho_converter_para_absoluto(diretorio_referencia)
        == "/home/pedro-pm-dias/Downloads/../../Downloads/Chrome/favoritos_23_12_2024.html"
    )


def test_pathlib_eh_arquivo(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_eh_arquivo() is True


def test_pathlib_eh_diretorio(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_eh_diretorio() is False


def test_pathlib_obter_nome(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_obter_nome() == "favoritos_23_12_2024.html"


def test_pathlib_obter_nome_sem_extensao(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_obter_nome_sem_extensao() == "favoritos_23_12_2024"


def test_pathlib_obter_extensao(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_obter_extensao() == ".html"


def test_pathlib_obter_pai(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert str(analisador.pathlib_obter_pai()) == "/home/pedro-pm-dias/Downloads/Chrome"


def test_pathlib_existe(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_existe() is True


def test_pathlib_eh_absoluto(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_eh_absoluto() is True


def test_pathlib_resolver_caminho(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert str(analisador.pathlib_resolver_caminho()) == str(
        Path(caminho_absoluto).resolve()
    )


def test_pathlib_contar_segmentos(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    assert analisador.pathlib_contar_segmentos() == 6


def test_obter_informacoes_combinadas(caminho_absoluto: str):
    analisador = AnalisadorPathlib(caminho_absoluto)
    informacoes = analisador.obter_informacoes_combinadas()
    assert informacoes["eh_absoluto"] is True
    assert informacoes["eh_valido"] is True
    assert informacoes["nome_arquivo"] == "favoritos_23_12_2024.html"
    assert informacoes["diretorio"] == "/home/pedro-pm-dias/Downloads/Chrome"
    assert informacoes["possui_extensao"] is True
    assert informacoes["contagem_segmentos"] == 5
    assert informacoes["eh_arquivo"] is True
    assert informacoes["eh_diretorio"] is False
    assert informacoes["nome"] == "favoritos_23_12_2024.html"
    assert informacoes["nome_sem_extensao"] == "favoritos_23_12_2024"
    assert informacoes["extensao"] == ".html"
    assert informacoes["pai"] == "/home/pedro-pm-dias/Downloads/Chrome"
    assert informacoes["metadados"]["existe"] is True
    assert informacoes["caminho_resolvido"] == str(Path(caminho_absoluto).resolve())
