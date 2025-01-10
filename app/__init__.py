"""
Arquivo __init__.py do pacote app.
"""

from flask import Flask
# from .config import Config
from .routes import main_routes


def create_app():
    """
    Função de fábrica para criar a instância do aplicativo Flask.
    """
    app = Flask(__name__)
    # app.config.from_object(Config)

    # Registrando blueprints
    app.register_blueprint(main_routes.bp)

    return app
