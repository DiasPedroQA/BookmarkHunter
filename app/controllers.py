# from flask import Blueprint, jsonify, request
# from app.services import analyze_path

# api = Blueprint("api", __name__)


# @api.route("/analyze", methods=["POST"])
# def analyze():
    # """Endpoint para analisar caminhos."""
    # data = request.get_json()
    # path = data.get("path")
    # if not path:
        # return jsonify({"error": "Path is required"}), 400

    # result = analyze_path(path)
    # return jsonify(result)


# def register_routes(app):
#     """Registra as rotas no app Flask."""
#     app.register_blueprint(api, url_prefix="/api")
