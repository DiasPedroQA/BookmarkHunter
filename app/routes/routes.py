# from flask import Blueprint
# from app.controllers import arquivo_controller
# from app.controllers.path_control import analyze_path_controller

# routes = Blueprint("routes", __name__)

# # Rotas de arquivos
# routes.route(
#     "/arquivos",
#     methods=["GET"]
# )(arquivo_controller.listar_arquivos)
# routes.route(
#     "/arquivos",
#     methods=["POST"]
# )(arquivo_controller.criar_arquivo)
# routes.route(
#     "/arquivos/<int:id>",
#     methods=["DELETE"]
# )(arquivo_controller.deletar_arquivo)

# # Rota para analisar caminhos
# routes = Blueprint("routes", __name__)

# @routes.route("/analyze", methods=["POST"])
# def analyze_route():
#     """
#     Rota para analisar caminhos.
#     """
#     return analyze_path_controller()
