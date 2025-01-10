# # tests/test_path_api.py
# # pylint: disable=C

# from flask.testing import FlaskClient
# import pytest
# from app.main import app

# @pytest.fixture
# def client_fixture():
#     app.config['TESTING'] = True
#     with app.test_client() as test_client:
#         yield test_client


# def test_index(new_client: FlaskClient):
#     response = new_client.get('/')
#     assert response.status_code == 200
#     assert "API de Validação de Caminhos".encode('utf-8') in response.data

# def test_validate_path_file(new_client: FlaskClient):
#     response = new_client.get('/validate?path=main.py')
#     assert response.status_code == 200
#     assert "É arquivo?".encode('utf-8') in response.data

# def test_validate_path_directory(new_client: FlaskClient):
#     response = new_client.get('/validate?path=controllers')
#     assert response.status_code == 200
#     assert "É pasta?".encode('utf-8') in response.data

# def test_missing_path(new_client: FlaskClient):
#     response = new_client.get('/validate')
#     assert response.status_code == 400
#     assert "O parâmetro 'path' é obrigatório".encode('utf-8') in response.data
