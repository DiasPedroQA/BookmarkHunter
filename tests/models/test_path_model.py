# pylint: disable=C, R, E, W

"""
Este módulo contém testes para o modelo de caminho (PathModel) da aplicação.
Os testes verificam a funcionalidade do modelo para diferentes tipos de caminhos,
incluindo caminhos absolutos e relativos, válidos e inválidos, arquivos e diretórios.

Testes incluídos:
- teste_caminho_absoluto_valido: Testa um caminho absoluto válido.
- teste_caminho_absoluto_invalido: Testa um caminho absoluto inválido.
- teste_caminho_absoluto_pasta: Testa um caminho absoluto de pasta.
- teste_caminho_absoluto_pasta_teste: Testa um caminho absoluto de pasta de teste.
- teste_caminho_absoluto_inexistente: Testa um caminho absoluto inexistente.
- test_caminho_relativo_valido: Testa um caminho relativo válido.
- test_caminho_relativo_invalido: Testa um caminho relativo inválido.
- test_caminho_relativo_pasta: Testa um caminho relativo de pasta.
- test_caminho_relativo_pasta_teste: Testa um caminho relativo de pasta de teste.
- test_caminho_relativo_inexistente: Testa um caminho relativo inexistente.
- test_inicialization_path_model: Testa a inicialização do modelo PathModel.
- test_caminho_valido: Testa a classe PathModel com um caminho válido.

"""

from typing import Dict
from app.models.path_model import PathModel
import json
import pytest
import pytest


def test_inicializacao_caminho_valido():
    """
    Testa se a classe aceita um caminho válido.
    """
    caminho_padrao = "../../Downloads/"
    modelo = PathModel(caminho=caminho_padrao)
    assert modelo.caminho_entrada == caminho_padrao


@pytest.mark.parametrize("caminho_invalido", [None, "", 123, [], {}, True])
def test_inicializacao_caminho_invalido(
    caminho_invalido: None | list | dict | str | int | bool,
):
    """
    Testa se a classe lança ValueError para caminhos inválidos.
    """
    with pytest.raises(ValueError) as erro_valor:
        PathModel(caminho=caminho_invalido)
    assert str(erro_valor.value) == "O caminho deve ser uma string não vazia."


def test_arquivo_simbolico_inexistente():
    arquivo_absoluto_link_simbolico_inexistente: str = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_link_simbólico.html"
    )
    modelo: PathModel = PathModel(caminho=arquivo_absoluto_link_simbolico_inexistente)
    arquivo_absoluto_tratado: str = modelo.tratar_link_simbolico(
        caminho_simbolico=modelo.caminho_entrada
    )
    arquivo_tratado: dict[str, str | dict[str, str | Dict[str, str | int]]] = json.loads(arquivo_absoluto_tratado)
    assert len(arquivo_tratado) == 3
    assert (
        arquivo_tratado["mensagem"]
        == f"O caminho '{arquivo_absoluto_link_simbolico_inexistente}' não é um link simbólico."
    )
    assert arquivo_tratado["status"] == "NOT_OK"
    assert arquivo_tratado["dados_caminho"] == {}


def test_pasta_simbolica_inexistente():
    pasta_absoluta_link_simbolico_inexistente: str = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_link_simbólico"
    )
    modelo: PathModel = PathModel(caminho=pasta_absoluta_link_simbolico_inexistente)
    pasta_absoluta_tratada: str = modelo.tratar_link_simbolico(
        caminho_simbolico=pasta_absoluta_link_simbolico_inexistente
    )
    pasta_tratada: dict[str, str | dict[str, str | Dict[str, str | int]]] = json.loads(pasta_absoluta_tratada)
    assert len(pasta_tratada) == 3
    assert (
        pasta_tratada["mensagem"]
        == f"O caminho '{pasta_absoluta_link_simbolico_inexistente}' não é um link simbólico."
    )
    assert pasta_tratada["status"] == "NOT_OK"
    assert pasta_tratada["dados_caminho"] == {}


teste_de_caminhos: dict[str, str] = {
    "arquivo_relativo_existente": "../../Downloads/Chrome/favoritos_23_12_2024.html",
    "arquivo_absoluto_existente": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
    "pasta_absoluta_existente": "/home/pedro-pm-dias/Downloads/",
    "arquivo_absoluto_inexistente": "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
    "arquivo_relativo_inexistente": "../../Downloads/Chrome/favoritos.html",
    "pasta_relativa_inexistente": "../../Downloads/Chrome2",
    "pasta_absoluta_inexistente": "/home/pedro-pm-dias/Downloads/Chrome2",
}



# converter_para_absoluto(arquivo_relativo_existente)
# tratar_caminho_relativo(arquivo_relativo_existente)
# converter_para_absoluto(pasta_relativa_existente)
# tratar_caminho_relativo(pasta_relativa_existente)

# tratar_caminho_existente(arquivo_absoluto_existente)
# validar_caminho(arquivo_absoluto_existente)
# obter_estatisticas(arquivo_absoluto_existente)
# determinar_tipo_caminho(arquivo_absoluto_existente)
# obter_pasta_mae(arquivo_absoluto_existente)

# tratar_caminho_existente(pasta_absoluta_existente)
# validar_caminho(pasta_absoluta_existente)
# obter_estatisticas(pasta_absoluta_existente)
# determinar_tipo_caminho(pasta_absoluta_existente)
# obter_pasta_mae(pasta_absoluta_existente)

# gerar_resposta_json()
# gerar_resposta_json()
