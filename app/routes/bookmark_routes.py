"""
Este módulo define as rotas relacionadas à funcionalidade de bookmarks para a API BookmarkHunter.

A rota inicial serve como um ponto de verificação para confirmar que a API está em execução.
As rotas adicionais permitem interações com bookmarks, como criação e consulta.
"""

from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models.bookmark_model import Marcador

# Criação do blueprint para as rotas relacionadas a bookmarks
bookmark_routes_bp = Blueprint("bookmark_routes", __name__)

# Dados simulados para teste (em produção, isso seria substituído por um banco de dados)
lista_bookmarks = []

@bookmark_routes_bp.route("/", methods=["GET"])
def home():
    """
    Rota inicial da API BookmarkHunter.

    Retorna uma mensagem indicando que a API está ativa e funcionando corretamente.

    Returns:
        tuple: Um dicionário com a mensagem de status e o código HTTP 200.
    """
    return {"message": "BookmarkHunter API is running!"}, 200


@bookmark_routes_bp.route("/bookmarks", methods=["POST"])
def create_bookmark():
    """
    Cria um novo bookmark com base nos dados enviados na requisição.
    """
    data = request.json
    try:
        bookmark = Marcador(
            titulo=data.get("title"),
            href=data.get("url"),
            data_adicao=datetime.fromisoformat(data.get("add_date")),
            ultima_modificacao=datetime.fromisoformat(data.get("last_modified")),
        )
        lista_bookmarks.append(bookmark)
        print(f"Bookmarks after addition: {lista_bookmarks}")  # Log
        return jsonify(
            {"message": "Marcador created successfully!", "bookmark": bookmark.to_json()}
            ), 201
    except ValueError as e:
        return jsonify({"error": f"Failed to create bookmark: Invalid date format - {str(e)}"}), 400
    except KeyError as e:
        return jsonify(
            {"error": f"Failed to create bookmark: Missing required field - {str(e)}"}
            ), 400
    except AttributeError as e:
        return jsonify(
            {"error": f"Failed to create bookmark: Invalid attribute - {str(e)}"}
            ), 400


@bookmark_routes_bp.route("/bookmarks", methods=["GET"])
def get_bookmarks():
    """
    Retorna a lista de todos os bookmarks disponíveis.
    """
    print(f"Current bookmarks: {lista_bookmarks}")  # Log
    bookmarks_json = [bookmark.to_json() for bookmark in lista_bookmarks]
    return jsonify({"bookmarks": bookmarks_json}), 200

@bookmark_routes_bp.route("/bookmarks", methods=["GET"])
def create_bookmark_with_get():
    """
    Cria um novo bookmark usando parâmetros de consulta na URL.
    """
    title = request.args.get("title")
    url = request.args.get("url")
    add_date = request.args.get("add_date")
    last_modified = request.args.get("last_modified")

    # Validação básica
    if not all([title, url, add_date, last_modified]):
        return {"error": "Missing required parameters."}, 400

    # Criar o bookmark
    try:
        bookmark = Marcador(
            titulo=title,
            href=url,
            data_adicao=datetime.fromisoformat(add_date),
            ultima_modificacao=datetime.fromisoformat(last_modified),
        )
        lista_bookmarks.append(bookmark)
        return {"message": "Marcador created successfully!", "bookmark": bookmark.to_json()}, 201
    except ValueError as e:
        return {"error": f"Failed to create bookmark: Invalid date format - {str(e)}"}, 400
    except AttributeError as e:
        return {"error": f"Failed to create bookmark: Invalid attribute - {str(e)}"}, 400
