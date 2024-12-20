# """
# Este módulo define as rotas relacionadas à funcionalidade de arquivos para a API BookmarkHunter.

# A rota inicial serve como um ponto de verificação para confirmar que a API está em execução.
# """

# # Importação do módulo Blueprint do Flask
# from flask import Blueprint

# # Criação do blueprint para as rotas relacionadas a arquivos
# file_routes_bp = Blueprint("file_routes", __name__)

# @file_routes_bp.route("/", methods=["GET"])
# def home():
#     """
#     Rota inicial da API BookmarkHunter.

#     Retorna uma mensagem indicando que a API está ativa e funcionando corretamente.

#     Returns:
#         tuple: Um dicionário com a mensagem de status e o código HTTP 200.
#     """
#     return {"message": "BookmarkHunter API is running!"}, 200
