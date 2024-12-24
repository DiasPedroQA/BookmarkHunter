# tests/backend/models/test_bookmark_model.py

"""
Testes para o modelo do objeto Tag.
"""

import os
import sys
import json


# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from app.models.bookmark_model import ObjetoTag


def test_inicializacao_objeto_tag():
    """
    Verifica se o objeto ObjetoTag é inicializado corretamente e contém as tags esperadas.
    """
    html_teste = """
    <html>
        <body>
            <h3>Test</h3>
            <a href="https://example.com">Link</a>
        </body>
    </html>
    """
    objeto = ObjetoTag(html_teste)
    assert isinstance(objeto, ObjetoTag)  # Verifica se o objeto é da classe ObjetoTag
    # assert len(objeto.tags) == 2  # Deve encontrar 2 tags: <h3> e <a>

def test_extrair_tags():
    """
    Verifica se o método _extrair_tags retorna as tags corretas.
    """
    html_teste = """
    <html>
        <body>
            <h3>Teste</h3>
            <a href="https://example.com">Link</a>
        </body>
    </html>
    """
    objeto = ObjetoTag(html_teste)
    json_tags = objeto.processar_tags()
    tags = json.loads(json_tags)
    assert len(tags) == 2  # Deve encontrar 2 tags: <h3> e <a>
    # assert isinstance(tags[0], Tag)  # A primeira tag deve ser do tipo Tag

def test_extrair_tags_sem_h3_ou_a():
    """
    Verifica se o método _extrair_tags não retorna tags quando não há tags <h3> ou <a>.
    """
    html_teste = "<html><body><p>Texto sem tags h3 ou a</p></body></html>"
    objeto = ObjetoTag(html_teste)
    json_tags = objeto.processar_tags()
    tags = json.loads(json_tags)
    assert len(tags) == 0  # Não deve encontrar tags <h3> ou <a>

def test_processar_tags():
    """
    Verifica se o método processar_tags processa corretamente todas as tags.
    """
    html_teste = """
    <html>
        <body>
            <h3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</h3>
            <a HREF="https://example.com">Link</a>
        </body>
    </html>
    """
    objeto = ObjetoTag(html_teste)
    resultado_json = objeto.processar_tags()

    # Verifica se o resultado é um JSON válido
    resultado_dict = json.loads(resultado_json)
    assert "tag_1" in resultado_dict  # Deve ter a chave 'tag_1' para a tag h3
    assert "tag_2" in resultado_dict  # Deve ter a chave 'tag_2' para a tag a
    assert isinstance(resultado_dict["tag_1"], dict)
    assert isinstance(resultado_dict["tag_2"], dict)

def test_processar_tags_empty_html():
    """
    Verifica se processar_tags retorna um JSON vazio para um HTML vazio.
    """
    processador = ObjetoTag(html="")
    resultado_processado = processador.processar_tags()
    assert resultado_processado == "{}"

def test_processar_tags_no_h3_or_a_tags():
    """
    Verifica se processar_tags retorna um JSON vazio quando não há tags <h3> ou <a>.
    """
    html_sem_tags = "<html><body><p>Sem tags relevantes</p></body></html>"
    processador = ObjetoTag(html=html_sem_tags)
    resultado_processado = processador.processar_tags()
    assert resultado_processado == "{}"

def test_processar_tags_with_only_h3_tags():
    """Verifica o processamento correto de um HTML contendo apenas tags <h3>."""
    html_h3_only = "<html><body><h3>Tag 1</h3><h3>Tag 2</h3></body></html>"
    processador = ObjetoTag(html=html_h3_only)
    resultado_processado = processador.processar_tags()
    dados = json.loads(resultado_processado)
    assert len(dados) == 2  # Deve ter 2 tags processadas
    assert "tag_1" in dados
    assert "tag_2" in dados

def test_processar_tags_with_only_a_tags():
    """Verifica o processamento correto de um HTML contendo apenas tags <a>."""
    html_a_only = "<html><body><a href='http://www.x.com'>Link 1</a><a href='http://www.y.org'>Link 2</a></body></html>"
    processador = ObjetoTag(html=html_a_only)
    resultado_processado = processador.processar_tags()
    dados = json.loads(resultado_processado)
    assert len(dados) == 2  # Deve ter 2 tags processadas
    assert "tag_1" in dados
    assert "tag_2" in dados

def test_processar_tags_with_add_date_and_last_modified():
    """Verifica se os atributos add_date e last_modified são processados corretamente."""
    html_com_datas = """
    <html>
        <body>
            <h3 add_date="1686621554" last_modified="1721823235">Estudos</h3>
            <a href="https://example.com" add_date="1686055702">Link</a>
        </body>
    </html>
    """
    processador = ObjetoTag(html=html_com_datas)
    resultado_processado = processador.processar_tags()
    dados = json.loads(resultado_processado)
    print(f"\n\nTESTE -> {dados}\n\n")

    # Verificando as conversões de data
    assert dados["tag_1"]["tag_name"] == "h3"
    assert dados["tag_1"]["text_content"] == "Estudos"
    assert dados["tag_1"]["attributes"]["add_date"] == "1686621554"
    assert dados["tag_1"]["attributes"]["last_modified"] == "1721823235"

    assert dados["tag_2"]["tag_name"] == "a"
    assert dados["tag_2"]["text_content"] == "Link"
    assert dados["tag_2"]["attributes"]["add_date"] == "1686055702"
    assert dados["tag_2"]["attributes"]["href"] == "https://example.com"

def test_processar_tags_with_malformed_html():
    """Verifica se o método lida com HTML malformado sem gerar exceções."""
    html_malformado = "<html><body><h3>Tag 1<p>Tag sem fechamento"
    processador = ObjetoTag(html=html_malformado)
    resultado_processado = processador.processar_tags()
    assert resultado_processado != "{}"  # Não deve retornar JSON vazio

def test_processar_tags_with_unknown_attributes():
    """Verifica se o processamento lida corretamente com atributos desconhecidos nas tags."""
    html_com_atributos_desconhecidos = """
    <html>
        <body>
            <h3 unknown_attr="value">Estudos</h3>
            <a href="https://example.com" unknown_attr="another_value">Link</a>
        </body>
    </html>
    """
    processador = ObjetoTag(html=html_com_atributos_desconhecidos)
    resultado_processado = processador.processar_tags()
    dados = json.loads(resultado_processado)

    # Verifica se as tags foram processadas corretamente, ignorando os atributos desconhecidos
    assert "tag_1" in dados
    assert "tag_2" in dados
    assert "unknown_attr" not in dados["tag_1"]
    assert "unknown_attr" not in dados["tag_2"]

def test_processar_tags_with_whitespace_text():
    """
    Verifica se o processamento lida corretamente
    com texto em branco ou espaços nas tags.
    """
    html_com_espacos = """
    <html>
        <body>
            <h3>   </h3>
            <a href="https://example.com">   </a>
        </body>
    </html>
    """
    processador = ObjetoTag(html=html_com_espacos)
    resultado_processado = processador.processar_tags()
    dados = json.loads(resultado_processado)

    # Verifica se o texto das tags foi removido corretamente
    assert dados["tag_1"]["text_content"] == ""
    assert dados["tag_2"]["text_content"] == ""
