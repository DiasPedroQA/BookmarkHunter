# tests/backend/models/test_file_model.py

"""
Testes para o modelo do objeto Arquivo.
"""

import os
import sys
import pytest


# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.models.file_model import ObjetoArquivo


def test_file_not_a_file():
    """
    Testa o comportamento ao tentar ler um caminho que não é um arquivo.
    """
    directory = ObjetoArquivo("/home/pedro-pm-dias/Downloads/Chrome/")
    with pytest.raises(ValueError, match="O caminho .* não é um arquivo."):
        directory.ler_caminho_arquivo()

def test_file_statistics_empty_content():
    """
    Testa a obtenção de estatísticas de um arquivo vazio, garantindo que os valores sejam zero.
    """
    file = ObjetoArquivo("/home/pedro-pm-dias/Downloads/Chrome/arquivo_vazio.txt")
    with open(file.caminho, "w", encoding="utf-8") as f:
        f.write("")
    stats = file.calcular_estatisticas("")
    assert stats["estatisticas"]["linhas"] == 0
    assert stats["estatisticas"]["palavras"] == 0
    assert stats["estatisticas"]["caracteres"] == 0


def test_file_info_not_exist():
    """
    Testa a obtenção de informações de um arquivo que não existe, garantindo que o retorno indique que não existe.
    """
    file = ObjetoArquivo("/caminho/invalido/para/arquivo.txt")
    info = file.obter_informacoes_path()
    assert info["existe"] is False


def test_file_info_exist():
    """
    Testa a obtenção de informações de um arquivo existente, garantindo que os dados retornados sejam corretos.
    """
    file = ObjetoArquivo(
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    )
    info = file.obter_informacoes_path()
    assert info["existe"] is True
    assert "tamanho" in info
    assert "modificado_em" in info
    assert "criado_em" in info
    assert "acessado_em" in info


# def test_mount_object_with_nonexistent_file():
#     """
#     Testa o comportamento ao montar um objeto para um arquivo inexistente.
#     """
#     file = ObjetoArquivo("/caminho/invalido/para/arquivo.txt")
#     result = file.montar_objeto()
#     assert result["path_info"]["existe"] is False


# def test_mount_object_with_empty_file():
#     """
#     Testa o comportamento ao montar um objeto para um arquivo vazio.
#     """
#     file = ObjetoArquivo("/home/pedro-pm-dias/Downloads/Chrome/arquivo_vazio.txt")
#     with open(file.caminho, "w", encoding="utf-8") as f:
#         f.write("")
#     result = file.montar_objeto()
#     assert result["estatisticas"]["linhas"] == 0
#     assert result["estatisticas"]["palavras"] == 0
#     assert result["estatisticas"]["caracteres"] == 0
