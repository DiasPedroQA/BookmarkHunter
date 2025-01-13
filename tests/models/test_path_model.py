# pylint: disable=C, R, E, W, W0105

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

"""
Este módulo contém testes para o modelo de caminho (PathModel) da aplicação.
Os testes verificam a funcionalidade do modelo para diferentes tipos de caminhos,
incluindo caminhos absolutos e relativos, válidos e inválidos, arquivos e diretórios.
"""

import json
import pytest
from pathlib import Path
from app.models.path_model import PathModel


@pytest.fixture
def criar_arquivo_tmp(tmp_path: Path):
    """
    Cria um arquivo temporário para os testes.
    :param tmp_path: Diretório temporário fornecido pelo pytest.
    :return: Caminho do arquivo criado.
    """
    arquivo = tmp_path / "arquivo_teste.txt"
    arquivo.write_text("Conteúdo de teste")
    return arquivo


@pytest.fixture
def criar_diretorio_tmp(tmp_path: Path):
    """
    Cria um diretório temporário para os testes.
    :param tmp_path: Diretório temporário fornecido pelo pytest.
    :return: Caminho do diretório criado.
    """
    diretorio = tmp_path / "diretorio_teste"
    diretorio.mkdir()
    return diretorio


def test_validar_caminho_vazio():
    path_model = PathModel("")
    result = path_model.validar_caminho()
    assert '"status": "ERROR"' in result
    assert '"mensagem": "Caminho vazio"' in result


def test_tratar_caminho_absoluto_arquivo_valido(criar_arquivo_tmp: Path):
    path_model = PathModel(str(criar_arquivo_tmp))
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "OK"
    assert dict_result["mensagem"] == "Caminho válido."
    assert dict_result["dados"]["tipo"] == "Arquivo"
    assert dict_result["dados"]["estatisticas"]["tamanho"] == "18.00 Bytes"


def test_tratar_caminho_absoluto_diretorio_valido(criar_diretorio_tmp: Path):
    path_model = PathModel(str(criar_diretorio_tmp))
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "OK"
    assert dict_result["mensagem"] == "Caminho válido."
    assert dict_result["dados"]["tipo"] == "Diretório"


def test_tratar_caminho_absoluto_inexistente():
    caminho_inexistente = "/caminho/que/nao/existe"
    path_model = PathModel(caminho_inexistente)
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "ERROR"
    assert dict_result["mensagem"] == f"Caminho '{caminho_inexistente}' não existe."


def test_tratar_caminho_relativo_valido(tmp_path: Path, criar_arquivo_tmp: Path):
    caminho_relativo = Path.cwd() / tmp_path / criar_arquivo_tmp
    path_model = PathModel(str(caminho_relativo))
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "OK"
    assert dict_result["mensagem"] == "Caminho válido."
    assert dict_result["dados"]["tipo"] == "Arquivo"


def test_tratar_caminho_relativo_inexistente():
    caminho_relativo_inexistente = "../diretorio/que/nao/existe"
    path_model = PathModel(caminho_relativo_inexistente)
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "ERROR"
    assert (
        dict_result["mensagem"] == f"Caminho relativo '{caminho_relativo_inexistente}' é inválido."
    )


def test_tratar_link_simbolico(tmp_path: Path):
    arquivo: Path = tmp_path / "arquivo_teste.txt"
    arquivo.write_text("Conteúdo de teste")
    link_simbolico = tmp_path / "link_teste"
    link_simbolico.symlink_to(arquivo)

    path_model = PathModel(str(link_simbolico))
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "OK"
    assert dict_result["mensagem"] == "Link simbólico resolvido com sucesso."
    assert dict_result["dados"]["tipo"] == "Arquivo"


def test_obter_estatisticas_arquivo(criar_arquivo_tmp: Path):
    path_model = PathModel(str(criar_arquivo_tmp))
    result = path_model.validar_caminho()
    dict_result = json.loads(result)
    assert dict_result["status"] == "OK"
    assert "estatisticas" in dict_result["dados"]
    assert dict_result["dados"]["estatisticas"]["tamanho"] == "18.00 Bytes"
