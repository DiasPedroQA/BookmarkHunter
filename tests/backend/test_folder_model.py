# tests/backend/test_folder_model.py

"""
Testes para o modelo de Bookmark
"""

import json
from app.models.bookmark_model import TagProcessor

# Teste para o processamento de múltiplas tags <h3> e <a> em sequência
def test_processar_multiple_tags():
    """
    Testa o processamento de múltiplas tags <h3> e <a> em sequência.
    """
    html = """
    <html>
        <body>
            <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
        <DL><p>
            <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702" ICON="data:image/png;base64,...">[pt-BR] Fundamentos do Git, um guia completo - DEV Community</A>
            <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
        <DL><p>
            <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793" ICON="data:image/png;base64,...">A Pirâmide do Teste Prático</A>
        </body>
    </html>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    # Verificando a primeira tag <h3>
    tag_h3_1 = resultado_dict["tag_1"]
    assert tag_h3_1["tag_name"] == "<h3>"
    assert tag_h3_1["text_content"] == "Estudos"
    assert tag_h3_1["add_date"] == "13/06/2023 01:59:14"
    assert tag_h3_1["last_modified"] == "24/07/2024 12:13:55"

    # Verificando a primeira tag <a>
    tag_a_1 = resultado_dict["tag_2"]
    assert tag_a_1["tag_name"] == "<a>"
    assert tag_a_1["text_content"] == "[pt-BR] Fundamentos do Git, um guia completo - DEV Community"
    assert tag_a_1["add_date"] == "06/06/2023 12:48:22"
    assert tag_a_1["href"] == "https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh"

    # Verificando a segunda tag <h3>
    tag_h3_2 = resultado_dict["tag_3"]
    assert tag_h3_2["tag_name"] == "<h3>"
    assert tag_h3_2["text_content"] == "Estudos"
    assert tag_h3_2["add_date"] == "13/06/2023 01:59:14"
    assert tag_h3_2["last_modified"] == "24/07/2024 12:13:55"

    # Verificando a segunda tag <a>
    tag_a_2 = resultado_dict["tag_4"]
    assert tag_a_2["tag_name"] == "<a>"
    assert tag_a_2["text_content"] == "A Pirâmide do Teste Prático"
    assert tag_a_2["add_date"] == "11/08/2023 07:09:53"
    assert tag_a_2["href"] == "https://martinfowler.com/articles/practical-test-pyramid.html"

# Teste para o processamento de tags <h3> com múltiplos atributos ADD_DATE e LAST_MODIFIED
def test_processar_multiple_attributes():
    """
    Testa o processamento de tags <h3> com múltiplos atributos ADD_DATE e LAST_MODIFIED.
    """
    html = """
    <h3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</h3>
    <h3 ADD_DATE="1708744361" LAST_MODIFIED="1731234567">Projetos</h3>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    # Verificando o primeiro <h3>
    tag_h3_1 = resultado_dict["tag_1"]
    assert tag_h3_1["tag_name"] == "<h3>"
    assert tag_h3_1["text_content"] == "Estudos"
    assert tag_h3_1["add_date"] == "13/06/2023 01:59:14"
    assert tag_h3_1["last_modified"] == "24/07/2024 12:13:55"

    # Verificando o segundo <h3>
    tag_h3_2 = resultado_dict["tag_2"]
    assert tag_h3_2["tag_name"] == "<h3>"
    assert tag_h3_2["text_content"] == "Projetos"
    assert tag_h3_2["add_date"] == "24/02/2024 03:12:41"
    assert tag_h3_2["last_modified"] == "10/11/2024 10:29:27"

# Teste para o processamento de tags <a> sem atributos ADD_DATE
def test_processar_tag_a_sem_add_date():
    """
    Testa o processamento de tags <a> sem o atributo ADD_DATE.
    """
    html = """
    <a href="https://example.com">Link do item sem data</a>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    # Verificando a tag <a> sem ADD_DATE
    tag_a = resultado_dict["tag_1"]
    assert tag_a["tag_name"] == "<a>"
    assert tag_a["text_content"] == "Link do item sem data"
    assert tag_a["add_date"] is not None  # Deve atribuir um valor padrão
    assert tag_a["href"] == "https://example.com"
    assert "last_modified" not in tag_a

# Teste para tratamento de data inválida em ADD_DATE
def test_processar_add_date_invalido():
    """
    Testa o processamento de ADD_DATE com valor inválido.
    """
    html = """
    <h3 ADD_DATE="invalid_date">Título com data inválida</h3>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado)

    # Verificando a tag <h3>
    tag_h3 = resultado_dict["tag_1"]
    assert tag_h3["add_date"] == "Formato inválido"  # A data deve ser tratada como inválida

# Teste para o processamento de tags <a> e <h3> sem ADD_DATE e LAST_MODIFIED
def test_processar_tag_sem_data():
    """
    Testa o processamento de tags <a> e <h3> sem ADD_DATE ou LAST_MODIFIED.
    """
    html = """
    <h3>Título sem data</h3>
    <a href="https://example.com">Link sem data</a>
    """
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    resultado_dict = json.loads(resultado, strict=False)

    # Verificando a tag <h3>
    tag_h3 = resultado_dict["tag_1"]
    print(f"\n\ntag_h3 => {tag_h3}")
    assert tag_h3["text_content"] == "Título sem data"
    assert tag_h3["add_date"] is not None  # Deve atribuir data padrão
    # assert tag_h3["last_modified"] == "Formato inválido"

    # Verificando a tag <a>
    tag_a = resultado_dict["tag_2"]
    print(f"\n\ntag_a => {tag_a}")
    assert tag_a["text_content"] == "Link sem data"
    assert tag_a["add_date"] is not None  # Deve atribuir data padrão
    assert tag_a["href"] == "https://example.com"
