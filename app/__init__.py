"""
Arquivo __init__.py do pacote app.
"""

from app.services import (
    obter_dados_caminho,
    obter_tamanho_arquivo,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
    obter_permissoes_caminho,
    obter_id_unico,
)

# from flask import Flask
# from flask_cors import CORS
# from controllers import register_routes


# def create_app():
#     """Inicializa a aplicação Flask."""
#     app = Flask(__name__)
#     CORS(app)
#     register_routes(app)
#     return app

__all__ = [
    "obter_dados_caminho",
    "obter_tamanho_arquivo",
    "obter_data_criacao",
    "obter_data_modificacao",
    "obter_data_acesso",
    "obter_permissoes_caminho",
    "obter_id_unico",
]
