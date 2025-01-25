# # pylint: disable=C0114, C0116, C2401

# import pytest
# from app.models.analisador_string import SanitizePath


# @pytest.mark.parametrize(
#     "caminho, esperado",
#     [
#         ("/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html", {
#             "caminho_original": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#             "caminho_sanitizado": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#             "formato_valido": True,
#             "eh_absoluto": True,
#             "eh_relativo": False,
#             "numero_diretorios": 4,
#             "nome_item": "favoritos_23_12_2024.html",
#             "pasta_principal": "Chrome",
#             "pasta_mae": "Downloads",
#             "eh_arquivo": True,
#             "eh_pasta": False,
#         }),
#         ("../imagens/foto.jpg", {
#             "caminho_original": "../imagens/foto.jpg",
#             "caminho_sanitizado": "../imagens/foto.jpg",
#             "formato_valido": True,
#             "eh_absoluto": False,
#             "eh_relativo": True,
#             "numero_diretorios": 1,
#             "nome_item": "foto.jpg",
#             "pasta_principal": "imagens",
#             "pasta_mae": "..",
#             "eh_arquivo": True,
#             "eh_pasta": False,
#         }),
#         ("/home/pedro-pm-dias/arquivo?*<>.html", {
#             "caminho_original": "/home/pedro-pm-dias/arquivo?*<>.html",
#             "caminho_sanitizado": "/home/pedro-pm-dias/arquivo.html",
#             "formato_valido": True,
#             "eh_absoluto": True,
#             "eh_relativo": False,
#             "numero_diretorios": 2,
#             "nome_item": "arquivo.html",
#             "pasta_principal": "pedro-pm-dias",
#             "pasta_mae": "home",
#             "eh_arquivo": True,
#             "eh_pasta": False,
#         }),
#         ("../imagens/arquivo?*<>.jpg", {
#             "caminho_original": "../imagens/arquivo?*<>.jpg",
#             "caminho_sanitizado": "../imagens/arquivo.jpg",
#             "formato_valido": True,
#             "eh_absoluto": False,
#             "eh_relativo": True,
#             "numero_diretorios": 1,
#             "nome_item": "arquivo.jpg",
#             "pasta_principal": "imagens",
#             "pasta_mae": "..",
#             "eh_arquivo": True,
#             "eh_pasta": False,
#         }),
#         ("/home/pedro-pm-dias/Downloads/Chrome/", {
#             "caminho_original": "/home/pedro-pm-dias/Downloads/Chrome/",
#             "caminho_sanitizado": "/home/pedro-pm-dias/Downloads/Chrome",
#             "formato_valido": True,
#             "eh_absoluto": True,
#             "eh_relativo": False,
#             "numero_diretorios": 3,
#             "nome_item": "Chrome",
#             "pasta_principal": "Downloads",
#             "pasta_mae": "pedro-pm-dias",
#             "eh_arquivo": False,
#             "eh_pasta": True,
#         }),
#         ("./Downloads/Chrome/", {
#             "caminho_original": "./Downloads/Chrome/",
#             "caminho_sanitizado": "./Downloads/Chrome",
#             "formato_valido": True,
#             "eh_absoluto": False,
#             "eh_relativo": True,
#             "numero_diretorios": 1,
#             "nome_item": "Chrome",
#             "pasta_principal": "Downloads",
#             "pasta_mae": ".",
#             "eh_arquivo": False,
#             "eh_pasta": True,
#         }),
#         ("/home/pedro-pm-dias/Downloads/Chrome/<>/", {
#             "caminho_original": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
#             "caminho_sanitizado": "/home/pedro-pm-dias/Downloads/Chrome",
#             "formato_valido": True,
#             "eh_absoluto": True,
#             "eh_relativo": False,
#             "numero_diretorios": 3,
#             "nome_item": "Chrome",
#             "pasta_principal": "Downloads",
#             "pasta_mae": "pedro-pm-dias",
#             "eh_arquivo": False,
#             "eh_pasta": True,
#         }),
#         ("./Downloads/Chrome/<>/", {
#             "caminho_original": "./Downloads/Chrome/<>/",
#             "caminho_sanitizado": "./Downloads/Chrome",
#             "formato_valido": True,
#             "eh_absoluto": False,
#             "eh_relativo": True,
#             "numero_diretorios": 1,
#             "nome_item": "Chrome",
#             "pasta_principal": "Downloads",
#             "pasta_mae": ".",
#             "eh_arquivo": False,
#             "eh_pasta": True,
#         }),
#     ],
# )

# def test_caminho(caminho: str, esperado: dict) -> None:
#     modelo = SanitizePath(caminho_original=caminho)
#     json_caminho = modelo.para_dict()

#     for chave, valor_esperado in esperado.items():
#         assert json_caminho.get(chave) == valor_esperado

# def test_caminho_excede_tamanho():
#     caminho = "a" * 261
#     with pytest.raises(ValueError, match="excede o limite de 260 caracteres"):
#         SanitizePath(caminho_original=caminho)

# @pytest.mark.parametrize("caminho", ["", "   ", "<>?|*", None])
# def test_caminho_invalido(caminho):
#     with pytest.raises(ValueError, match="caminho inválido"):
#         SanitizePath(caminho_original=caminho)

# @pytest.mark.parametrize("caminho, esperado", [
#     ("/", {"eh_absoluto": True, "numero_diretorios": 0}),
#     ("../", {"eh_relativo": True, "numero_diretorios": 0}),
#     ("/home/user/", {"pasta_principal": "user", "pasta_mae": "home"}),
# ])
# def test_caminho_borda(caminho: str, esperado: dict[str, bool | int] | dict[str, str]):
#     modelo = SanitizePath(caminho_original=caminho)
#     for chave, valor in esperado.items():
#         assert getattr(modelo, chave) == valor
