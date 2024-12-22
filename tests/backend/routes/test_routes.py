# """
# Este módulo contém testes para a rota home da API.

# Classes:
#     TestHomeRoute: Testa a rota home da API.
# """

# import pytest
# from flask import Flask
# from app.routes.file_routes import file_routes_bp

# # Criando uma instância do app com a blueprint registrada
# @pytest.fixture
# def create_app():
#     """
#     Cria uma instância do app com a blueprint registrada.
#     """
#     flask_app = Flask(__name__)
#     flask_app.register_blueprint(file_routes_bp, url_prefix="/api")
#     return flask_app

# # Teste para verificar se a rota home está funcionando corretamente
# def test_home_route(client):
#     """
#     Testa se a rota home está funcionando corretamente.
#     """
#     # Fazendo uma requisição GET para a rota '/'
#     response = client.get('/api/')

#     # Verificando se a resposta é bem-sucedida (status code 200)
#     assert response.status_code == 200

#     # Verificando se o conteúdo da resposta está correto
#     assert response.json == {"message": "BookmarkHunter API is running!"}
