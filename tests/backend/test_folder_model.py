# tests/backend/test_folder_model.py

"""
Testes para o modelo de Bookmark
"""

import json
from app.models.bookmark_model import TagProcessor


# Teste para o processamento de tags <h3> (título de lista de Bookmark)
def test_processar_tag_h3():
    """
    Testa o processamento de tags <h3> (título de lista de Bookmark).
    """
    html = """
    <h3 ADD_DATE="1726278565" LAST_MODIFIED="1726278565">Título da lista</h3>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    # Verificando a tag <h3>
    tag_h3 = resultado_dict["tag_1"]
    assert tag_h3["tag_name"] == "h3"
    assert tag_h3["text_content"] == "Título da lista"
    assert tag_h3["add_date"] == "14/09/2024 01:49:25"  # Horário em UTC
    assert tag_h3["last_modified"] == "14/09/2024 01:49:25"
    assert "href" not in tag_h3  # Não deve ter o atributo href


# Teste para o processamento de tags <a> (itens de Bookmark)
def test_processar_tag_a():
    """
    Testa o processamento de tags <a> (itens de Bookmark).
    """
    html = """
    <a href="https://example.com" ADD_DATE="1708744361">Link do item</a>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    # Verificando a tag <a>
    tag_a = resultado_dict["tag_1"]
    assert tag_a["tag_name"] == "a"
    assert tag_a["text_content"] == "Link do item"
    assert tag_a["add_date"] == "24/02/2024 03:12:41"  # Verifique o timestamp correto
    assert tag_a["href"] == "https://example.com"
    assert "last_modified" not in tag_a  # Não deve ter o atributo last_modified


# Teste para garantir que o JSON gerado tem a estrutura correta
def test_json_gerado():
    """
    Testa se o JSON gerado tem a estrutura correta.
    """
    html = """
    <h3 ADD_DATE="1726278565">Título 1</h3>
    <a href="https://example.com" ADD_DATE="1708744361">Link 1</a>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()

    # Verificando se o JSON tem as chaves corretas
    resultado_dict = json.loads(resultado)
    assert "tag_1" in resultado_dict
    assert "tag_2" in resultado_dict
    assert "id" in resultado_dict["tag_1"]
    assert "text_content" in resultado_dict["tag_1"]
    assert "add_date" in resultado_dict["tag_1"]
    assert "tag_name" in resultado_dict["tag_1"]
    assert "last_modified" in resultado_dict["tag_1"]  # Para <h3>
    assert "href" in resultado_dict["tag_2"]  # Para <a>


# Teste para validar a formatação JSON do resultado
def test_json_formatado():
    """
    Testa se o JSON gerado está formatado corretamente.
    """
    html = """
    <h3 ADD_DATE="1726278565">Título 1</h3>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()

    # Verificando se o JSON está formatado com indentação
    assert resultado.startswith("{")
    assert resultado.endswith("}")
    assert "\n" in resultado  # Deve ter quebras de linha por causa da indentação


# Teste para tratar timestamps inválidos
def test_timestamp_invalido():
    """
    Testa se o timestamp inválido é tratado corretamente.
    """
    html = '<h3 ADD_DATE="invalid_timestamp">Título</h3>'
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    tag_h3 = resultado_dict["tag_1"]
    assert tag_h3["add_date"] == "Formato inválido"


# Teste para tags sem atributos ADD_DATE e LAST_MODIFIED
def test_tags_sem_atributos():
    """
    Testa o comportamento de tags sem atributos ADD_DATE ou LAST_MODIFIED.
    """
    html = """
    <h3>Título sem data</h3>
    <a href="https://example.com">Link sem data</a>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    tag_h3 = resultado_dict["tag_1"]
    assert tag_h3["text_content"] == "Título sem data"
    assert tag_h3["add_date"] is not None
    assert tag_h3["last_modified"] == "Formato inválido"

    tag_a = resultado_dict["tag_2"]
    assert tag_a["text_content"] == "Link sem data"
    assert tag_a["add_date"] is not None
    assert tag_a["href"] == "https://example.com"
