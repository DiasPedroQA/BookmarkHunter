# app/routes/path_routes.py

"""
Rotas para processar caminhos.
"""

import json
from flask import Blueprint, request, jsonify
from app.services.path_service import PathService

bp = Blueprint("path_routes", __name__)
service = PathService()

@bp.route("/paths/process", methods=["POST"])
def process_paths():
    """Rota para processar caminhos."""
    data = request.get_json()

    if not data or "jsonEntrada" not in data:
        return jsonify({"error": "Entrada JSON inválida ou ausente"}), 400

    try:
        resultados = service.processar_caminhos(json.dumps(data))
        return jsonify({"resultados": resultados}), 200
    except (TypeError, ValueError, KeyError, json.JSONDecodeError) as e:
        return jsonify({"error": "Erro ao processar dados", "details": str(e)}), 400
