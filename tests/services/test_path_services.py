# # pylint: disable=C, R, E, W

# """
# Testes para as funções do módulo services.py.
# """

# import pytest
# from app.services.file_services import obter_tamanho_arquivo
# from app.services.path_services import (
#     obter_dados_caminho,
#     obter_permissoes_caminho,
#     obter_id_unico,
#     sanitizar_caminho_relativo,
#     fatiar_caminho,
# )


# def test_obter_dados_caminho_arquivo():
#     caminho = "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
#     esperado = {
#         "pasta_pai": "home/pedro-pm-dias/Downloads/Chrome",
#         "extensao_arquivo": "html",
#         "nome_arquivo": "favoritos_23_12_2024",
#     }
#     resultado = obter_dados_caminho(caminho)
#     assert resultado == esperado


# def test_obter_dados_caminho_vazio():
#     caminho = ""
#     esperado = {
#         "pasta_pai": "",
#         # "extensao_arquivo": "",
#         # "nome_arquivo": "",
#     }
#     resultado = obter_dados_caminho(caminho)
#     assert resultado == esperado


# def test_obter_dados_caminho_invalido():
#     caminho = None
#     with pytest.raises(ValueError):
#         obter_dados_caminho(caminho)


# def test_obter_tamanho_arquivo_bytes():
#     tamanho = 500
#     esperado = "500.00 Bytes"
#     assert obter_tamanho_arquivo(tamanho) == esperado


# def test_obter_tamanho_arquivo_kb():
#     tamanho = 2048
#     esperado = "2.00 KB"
#     assert obter_tamanho_arquivo(tamanho) == esperado


# def test_obter_tamanho_arquivo_invalido():
#     tamanho = 0
#     with pytest.raises(ValueError):
#         obter_tamanho_arquivo(tamanho)


# def test_fatiar_caminho_valido():
#     caminho = "/home/user/docs/"
#     esperado = ["home", "user", "docs"]
#     assert fatiar_caminho(caminho) == esperado


# def test_fatiar_caminho_invalido():
#     caminho = 123
#     with pytest.raises(ValueError):
#         fatiar_caminho(caminho)


# def test_obter_permissoes_caminho_leitura_escrita_execucao():
#     caminho = "/tmp"
#     esperado = {"leitura": True, "escrita": True, "execucao": True}
#     assert obter_permissoes_caminho(caminho) == esperado


# def test_obter_permissoes_caminho_inexistente():
#     caminho = "/path/inexistente"
#     esperado = {"leitura": False, "escrita": False, "execucao": False}
#     assert obter_permissoes_caminho(caminho) == esperado


# def test_obter_id_unico_valido():
#     identificador = 12345
#     esperado_tamanho = 36
#     id_unico = obter_id_unico(identificador)
#     assert isinstance(id_unico, str)
#     assert len(id_unico) == esperado_tamanho


# def test_obter_id_unico_invalido():
#     identificador = -1
#     with pytest.raises(ValueError):
#         obter_id_unico(identificador)


# def test_sanitizar_caminho_relativo_valido():
#     caminho = "../relative/path"
#     esperado = "relative/path"
#     assert sanitizar_caminho_relativo(caminho) == esperado


# def test_sanitizar_caminho_relativo_vazio():
#     caminho = ""
#     esperado = ""
#     assert sanitizar_caminho_relativo(caminho) == esperado
