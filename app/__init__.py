"""
Arquivo __init__.py do pacote app.
"""

# from flask import Flask, jsonify, request
# from app.routes.routes import routes
# from app.controllers.path_control import Path_Controller
# from app.controllers.file_control import listar_arquivos, criar_arquivo, deletar_arquivo

# def create_app():
#     """
#     Inicializa e configura a aplicação Flask.

#     Retorna:
#         app (Flask): A aplicação Flask configurada.
#     """
#     app = Flask(__name__)

#     # Registro de rotas utilizando Blueprint
#     app.register_blueprint(routes, url_prefix="/api")

#     # Rota para analisar caminhos
#     @app.route("/analyze", methods=["POST"])
#     def analyze():
#         """
#         Rota para analisar caminhos.
#         """
#         data = request.get_json()
#         path = data.get("path")
#         if not path:
#             return jsonify({"error": "Path is required"}), 400
#         controle = Path_Controller(path)
#         return jsonify({
#             "caminho_absoluto": controle._caminho_atual,
#             "caminho_relativo": controle.caminho_entrada
#         })

#     # Rota para listar arquivos
#     @app.route("/arquivos", methods=["GET"])
#     def listar_arquivos_route():
#         """
#         Rota para listar arquivos.
#         """
#         return listar_arquivos()

#     # Rota para criar arquivo
#     @app.route("/arquivos", methods=["POST"])
#     def criar_arquivo_route():
#         """
#         Rota para criar arquivo.
#         """
#         return criar_arquivo()

#     # Rota para deletar arquivo
#     @app.route("/arquivos/<int:id>", methods=["DELETE"])
#     def deletar_arquivo_route(id):
#         """
#         Rota para deletar arquivo.
#         """
#         return deletar_arquivo(id)

#     return app
