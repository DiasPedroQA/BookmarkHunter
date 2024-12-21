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
    assert tag_h3["add_date"] == "13/09/2024 18:22:45"
    assert tag_h3["last_modified"] == "13/09/2024 18:22:45"
    assert "href" not in tag_h3  # Não deve ter atributo href


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
    assert tag_a["add_date"] == "24/02/2024 02:52:41"
    assert tag_a["href"] == "https://example.com"
    assert "last_modified" not in tag_a  # Não deve ter atributo last_modified


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
    assert '\n' in resultado  # Deve ter quebras de linha por causa da indentação

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
