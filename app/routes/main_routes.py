# pylint: disable=C
# app/routes/main_routes.py

"""
Este módulo define as rotas relacionadas
à análise de texto e caminhos de arquivos.
"""

from flask import Blueprint, render_template, request
from app.services.text_analysis import analyze_text
from app.services.file_manager import analyze_paths
from flask import Blueprint, jsonify, request
from app.controllers.analysis_controller import AnalysisController
from flask import Blueprint, request, jsonify
from app.controllers.file_controller import FileController

bp = Blueprint("file_routes", __name__)
controller = FileController()

@bp.route("/files/analyze", methods=["POST"])
def analyze_files():
    """Rota para analisar arquivos ou pastas."""
    data = request.get_json()
    path = data.get("path")

    if not path:
        return jsonify({"error": "O caminho é obrigatório"}), 400

    try:
        result = controller.analyze_path(path)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


bp = Blueprint("main_routes", __name__)
controller = AnalysisController()


@bp.route("/process", methods=["POST"])
def processar_dados():
    """Rota para processar dados recebidos"""
    dados = request.get_json()
    resultado = controller.processar_dados(dados)
    return jsonify(resultado)


# Definindo o Blueprint. O nome do blueprint é "analysis".
bp = Blueprint("analysis", __name__, url_prefix="/")


@bp.route("/", methods=["GET"])
def home():
    """
    Renderiza a página inicial.
    """
    return render_template("index.html")


@bp.route("/analyze_text", methods=["POST"])
def analyze_text_route():
    """
    Recebe texto enviado pelo cliente e retorna o resultado da análise.
    """
    text = request.form.get("text")
    if not text:
        return "Nenhum texto fornecido.", 400
    result = analyze_text(text)
    return render_template("result.html", result=result)


@bp.route("/analyze_paths", methods=["POST"])
def analyze_paths_route():
    """
    Recebe caminhos enviados pelo cliente e retorna o resultado da análise.
    """
    paths = request.form.getlist("paths")
    if not paths:
        return "Nenhum caminho fornecido.", 400
    result = analyze_paths(paths)
    return render_template("result.html", result=result)
