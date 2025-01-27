# pylint: disable=C, R, E, W

from app.models.path_model import CaminhoBase
from app.services.path_services import RegexPathAnalyzer
import json

"""
Os testes verificam a funcionalidade do modelo para diferentes tipos de caminhos,
incluindo caminhos absolutos e relativos, válidos e inválidos, arquivos e diretórios.
"""


# Testando a inicialização do objeto CaminhoBase
def test_caminho_base_init():
    caminho = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    caminho_obj = CaminhoBase(caminho_bruto=caminho)
    assert caminho_obj.caminho_original == caminho


# Testando o método obter_id_unico
def test_obter_id_unico():
    caminho = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    id_unico = CaminhoBase.obter_id_unico(caminho)
    assert isinstance(id_unico, str)
    assert len(id_unico) == 36  # UUID length


# Testando o método para_dict
def test_para_dict(mocker):
    caminho = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    caminho_obj = CaminhoBase(caminho_bruto=caminho)

    mocker.patch.object(RegexPathAnalyzer, "analisar_caminho", return_value="analisado")
    caminho_obj.caminho_analisado = "analisado"

    caminho_dict = caminho_obj.para_dict()
    assert isinstance(caminho_dict, dict)
    assert caminho_dict["caminho_original"] == caminho
    assert "id_unico" in caminho_dict
    assert isinstance(caminho_dict["analises_caminho"], RegexPathAnalyzer)


# Testando o método gerar_json
def test_gerar_json(mocker):
    caminho = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    caminho_obj = CaminhoBase(caminho_bruto=caminho)

    mocker.patch.object(RegexPathAnalyzer, "analisar_caminho", return_value="analisado")
    caminho_obj.caminho_analisado = "analisado"

    caminho_json = caminho_obj.gerar_json()
    assert isinstance(caminho_json, str)
    caminho_dict = json.loads(caminho_json)
    assert caminho_dict["caminho_original"] == caminho
    assert "id_unico" in caminho_dict
    assert "analises_caminho" in caminho_dict


# Testando o método _processar_caminho
def test_processar_caminho(mocker):
    caminho = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    caminho_obj = CaminhoBase(caminho_bruto=caminho)

    mocker.patch.object(RegexPathAnalyzer, "analisar_caminho", return_value="analisado")
    caminho_obj._processar_caminho()

    assert caminho_obj.caminho_analisado == "analisado"
