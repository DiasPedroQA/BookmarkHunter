# pylint: disable=C, R, E, W

from pathlib import Path

from flask import Blueprint, jsonify, request
from app.services import analyze_path

api = Blueprint("api", __name__)

@api.route("/analyze", methods=["POST"])
def analyze():
    """Endpoint para analisar caminhos."""
    data = request.get_json()
    path = data.get("path")
    if not path:
        return jsonify({"error": "Path is required"}), 400

    result = analyze_path(path)
    return jsonify(result)

def register_routes(app):
    """Registra as rotas no app Flask."""
    app.register_blueprint(api, url_prefix="/api")


class Path_Controller:
    """
    Classe que gerencia as operações relacionadas a caminhos.
    """

    def __init__(self, entrada: str):
        """
        Inicializa o controlador de caminhos.
        """
        self._caminho_atual = Path.cwd()
        self.caminho_entrada = entrada


caminhos = {
    "caminho_absoluto_pasta": "/home/pedro-pm-dias/Downloads/",
    "caminho_relativo_pasta": "../../Downloads/"
}

for tipo_caminho, valor_caminho in caminhos.items():
    print("-" * 40)
    print(f"Tipo de Caminho: {tipo_caminho}")
    controle = Path_Controller(valor_caminho)
    print(f"Valor do Caminho: {controle._caminho_atual}")
    print(f"Valor do Caminho: {controle.caminho_entrada}")

