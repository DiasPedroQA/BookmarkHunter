# pylint: disable=C, R, E, W

"""
Os testes verificam a funcionalidade do modelo para diferentes tipos de caminhos,
incluindo caminhos absolutos e relativos, válidos e inválidos, arquivos e diretórios.
"""

from app.models.path_model import CaminhoUtils
import pytest
from pathlib import Path


# Testando o método validar_caminho_como_string
def test_validar_caminho_como_string():
    # Caminhos válidos
    assert CaminhoUtils.validar_caminho_como_string("./") == False
    assert CaminhoUtils.validar_caminho_como_string(".") == False
    assert CaminhoUtils.validar_caminho_como_string(".venv") == True
    assert CaminhoUtils.validar_caminho_como_string("../Downloads") == True
    assert CaminhoUtils.validar_caminho_como_string("../Downloads/") == True
    assert CaminhoUtils.validar_caminho_como_string("/../Downloads") == True
    assert CaminhoUtils.validar_caminho_como_string("/../Downloads/") == True
    assert CaminhoUtils.validar_caminho_como_string("/../") == True

    # Caminhos inválidos
    assert CaminhoUtils.validar_caminho_como_string(0) == False
    assert CaminhoUtils.validar_caminho_como_string(-42) == False
    assert CaminhoUtils.validar_caminho_como_string(123) == False
    assert CaminhoUtils.validar_caminho_como_string(None) == False
    assert CaminhoUtils.validar_caminho_como_string([]) == False
    assert CaminhoUtils.validar_caminho_como_string(()) == False
    assert CaminhoUtils.validar_caminho_como_string({}) == False
    assert CaminhoUtils.validar_caminho_como_string(True) == False
    assert CaminhoUtils.validar_caminho_como_string(False) == False



# Testando o método converter_para_absoluto
def test_converter_para_absoluto():
    # Caminhos válidos (você pode alterar o valor para o seu diretório)
    caminho_relativo = "./"
    caminho_absoluto = CaminhoUtils.converter_para_absoluto(caminho_relativo)
    assert caminho_absoluto == str(
        (Path.home() / Path(caminho_relativo.lstrip("./"))).resolve()
    )

    # Caminhos inválidos
    assert CaminhoUtils.converter_para_absoluto("") == ""
    assert CaminhoUtils.converter_para_absoluto(None) == ""
    assert CaminhoUtils.converter_para_absoluto(123) == ""


# Testando o método gerar_resposta_json
def test_gerar_resposta_json():
    resposta = CaminhoUtils.gerar_resposta_json(
        mensagem="Teste de sucesso",
        status="SUCCESS",
        caminhos_validados={"./": True},
        caminhos_convertidos={"./": "/home/user/test"},
    )

    assert isinstance(resposta, str)  # A resposta deve ser uma string.
    assert (
        "mensagem" in resposta
    )  # Verifica se a chave "mensagem" está presente no JSON.
    assert "status" in resposta  # Verifica se a chave "status" está presente no JSON.
    assert (
        "dados_caminho" in resposta
    )  # Verifica se a chave "dados_caminho" está presente no JSON.
    assert (
        '"mensagem": "Teste de sucesso"' in resposta
    )  # Verifica o valor da chave "mensagem".

    # Testando o erro quando a mensagem é inválida
    with pytest.raises(ValueError):
        CaminhoUtils.gerar_resposta_json(mensagem="", status="SUCCESS")

    with pytest.raises(ValueError):
        CaminhoUtils.gerar_resposta_json(mensagem="Teste", status=123)


# Testando o filtro de caminhos validados
def test_filtrar_caminhos_validados():
    caminhos_validados = {
        "./": True,
        "../Downloads": False,
        "/../Downloads": True,
        "/./": False,
    }

    caminhos_validados_true = {
        chave: valor for chave, valor in caminhos_validados.items() if valor is True
    }

    assert caminhos_validados_true == {"./": True, "/../Downloads": True}


# Testando o filtro de caminhos convertidos
def test_filtrar_caminhos_convertidos():
    caminhos_convertidos = {
        "./": "/home/user/test",
        "../Downloads": "/home/user/Downloads",
        "/../Downloads": "/home/user/Downloads",
        "/./": "/home/user",
    }

    caminhos_convertidos_diferentes = {
        chave: valor for chave, valor in caminhos_convertidos.items() if chave != valor
    }

    assert caminhos_convertidos_diferentes == {
        "./": "/home/user/test",  # A chave é diferente do valor
    }
