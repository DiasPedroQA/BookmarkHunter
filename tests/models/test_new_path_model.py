# pylint: disable=C, R, E, W

import pytest
from pathlib import Path
from app.models.new_path_model import AnalisadorCaminhoIntegrado


"""
Testes para a classe AnalisadorCaminhoIntegrado.

Funções de teste:
- setup_analisador: Fixture do pytest para configurar o objeto AnalisadorCaminhoIntegrado.
- test_eh_absoluto: Verifica se o caminho não é absoluto.
- test_eh_relativo: Verifica se o caminho é relativo.
- test_eh_valido: Verifica se o caminho é válido.
- test_obter_nome: Verifica se o nome do arquivo é obtido corretamente.
- test_obter_nome_sem_extensao: Verifica se o nome do arquivo sem extensão é obtido corretamente.
- test_obter_extensao: Verifica se a extensão do arquivo é obtida corretamente.
- test_obter_diretorio_pai: Verifica se o diretório pai é obtido corretamente.
- test_possui_extensao: Verifica se o arquivo possui a extensão especificada.
- test_contar_segmentos: Verifica se a contagem de segmentos do caminho está correta.
- test_obter_metadados: Verifica se os metadados do arquivo são obtidos corretamente (assume que o arquivo não existe).
- test_resolver_caminho: Verifica se o caminho é resolvido para um caminho absoluto.
- test_converter_para_relativo: Verifica se o caminho é convertido corretamente para um caminho relativo.
- test_converter_para_absoluto: Verifica se o caminho é convertido corretamente para um caminho absoluto.
- test_obter_informacoes_combinadas: Verifica se as informações combinadas do caminho são obtidas corretamente.
"""


@pytest.fixture
def setup_analisador():
    caminho = "../../Downloads/Chrome/favoritos_23_12_2024.html"
    referencia_dir = "/home/pedro-pm-dias/Downloads/Chrome"
    return AnalisadorCaminhoIntegrado(
        caminho_inicial=caminho, referencia_dir=referencia_dir
    )


def test_eh_absoluto(setup_analisador: AnalisadorCaminhoIntegrado):
    assert not setup_analisador.eh_absoluto()


def test_eh_relativo(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.eh_relativo()


def test_eh_valido(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.eh_valido()


def test_obter_nome(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.obter_nome() == "favoritos_23_12_2024.html"


def test_obter_nome_sem_extensao(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.obter_nome_sem_extensao() == "favoritos_23_12_2024"


def test_obter_extensao(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.obter_extensao() == ".html"


def test_obter_diretorio_pai(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.obter_diretorio_pai() == "../../Downloads/Chrome"


def test_possui_extensao(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.possui_extensao(".html")


def test_contar_segmentos(setup_analisador: AnalisadorCaminhoIntegrado):
    assert setup_analisador.contar_segmentos() == 5


def test_obter_metadados(setup_analisador: AnalisadorCaminhoIntegrado):
    # This test assumes the file does not exist
    assert setup_analisador.obter_metadados() == {}


def test_resolver_caminho(setup_analisador: AnalisadorCaminhoIntegrado):
    resolved_path = setup_analisador.resolver_caminho()
    assert Path(resolved_path).is_absolute()


def test_converter_para_relativo(setup_analisador: AnalisadorCaminhoIntegrado):
    assert (
        setup_analisador.converter_para_relativo()
        == "../../Downloads/Chrome/favoritos_23_12_2024.html"
    )


def test_converter_para_absoluto(setup_analisador: AnalisadorCaminhoIntegrado):
    absolute_path = setup_analisador.converter_para_absoluto()
    assert Path(absolute_path).is_absolute()


def test_obter_informacoes_combinadas(setup_analisador: AnalisadorCaminhoIntegrado):
    """
    Testa a função obter_informacoes_combinadas do objeto setup_analisador.

    Este teste verifica se as informações combinadas retornadas pela função
    obter_informacoes_combinadas estão corretas. Asserções são feitas para
    garantir que cada campo do dicionário de informações esteja de acordo
    com os valores esperados.

    Asserções:
        - informacoes["eh_absoluto"] deve ser False
        - informacoes["eh_valido"] deve ser True
        - informacoes["nome_caminho"] deve ser "favoritos_23_12_2024.html"
        - informacoes["diretorio_pai"] deve ser "../../Downloads/Chrome"
        - informacoes["extensao"] deve ser ".html"
        - informacoes["possui_extensao"] deve ser True
        - informacoes["contagem_segmentos"] deve ser 5
        - informacoes["eh_arquivo"] deve ser False
        - informacoes["eh_diretorio"] deve ser False
        - informacoes["nome_sem_extensao"] deve ser "favoritos_23_12_2024"
        - informacoes["caminho_relativo"] deve ser "favoritos_23_12_2024.html"
        - informacoes["caminho_absoluto"] deve ser um caminho absoluto
    """
    informacoes = setup_analisador.obter_informacoes_combinadas()
    assert informacoes["eh_absoluto"] == False
    assert informacoes["eh_valido"] == True
    assert informacoes["nome_caminho"] == "favoritos_23_12_2024.html"
    assert informacoes["diretorio_pai"] == "../../Downloads/Chrome"
    assert informacoes["extensao"] == ".html"
    assert informacoes["possui_extensao"] == True
    assert informacoes["contagem_segmentos"] == 5
    assert informacoes["eh_arquivo"] == False
    assert informacoes["eh_diretorio"] == False
    assert informacoes["nome_sem_extensao"] == "favoritos_23_12_2024"
    assert (
        informacoes["caminho_relativo"]
        == "favoritos_23_12_2024.html"
    )
    assert Path(informacoes["caminho_absoluto"]).is_absolute()
