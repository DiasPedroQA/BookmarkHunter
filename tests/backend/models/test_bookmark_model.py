# tests/backend/models/test_bookmark_model.py

"""
Módulo de testes para o processamento de tags HTML.

Este módulo utiliza a biblioteca pytest para validar a funcionalidade das classes
presentes no arquivo bookmark_model.py. Ele cobre cenários de processamento de
tags válidas (<h3> e <a>), conversão de atributos e formatação em JSON.

Funções:
    test_instanciacao(): Valida a instância de ObjetoTag.
    test_extracao_tags(): Testa a extração de tags válidas.
    test_processamento_atributos(): Verifica a conversão de atributos das tags.
    test_processar_tags(): Garante que o JSON gerado está formatado corretamente.
"""

import os
import sys
import pytest

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413, W0212, W0621
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.models.bookmark_model import BaseTagModel, ObjetoTag


@pytest.fixture
def html_teste() -> str:
    """
    Retorna um HTML de teste com tags válidas (<h3> e <a>) e atributos variados.

    Returns:
        str: HTML contendo tags para teste.
    """
    return """
    <html>
        <body>
            <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
            <DL><p>
                <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
                <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
            <DL><p>
                <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
            </body>
    </html>
    """


def test_processar_atributos_com_timestamps(html_teste: str):
    processador = ObjetoTag(html_content=html_teste)
    tags = processador._extrair_tags()
    atributos_tag1 = processador._processar_atributos(tags[0])
    atributos_tag1["add_date"] = "1686621554"  # Timestamp for testing
    processador._tag_atributos = atributos_tag1
    processador.processar_atributos_com_timestamps()
    assert atributos_tag1["add_date"] == "12/06/2023 22:59:14"

def test_raspar_e_processar_tags(html_teste: str):
    processador = ObjetoTag(html_content=html_teste)
    resultado = processador.raspar_e_processar_tags()
    assert len(resultado) == 4
    assert resultado[0]["name"] == "h3"
    assert resultado[1]["attributes"]["href"] == "https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh"

def test_dados_definidos_false():
    tag = BaseTagModel()
    assert not tag.dados_definidos()

def test_dados_definidos_true():
    tag = BaseTagModel()
    tag.tag_name = "h3"
    tag.tag_text_content = "Test"
    tag.tag_atributos = {"add_date": "1686621554"}
    assert tag.dados_definidos()

def test_criar_objeto_tag():
    html_teste = "<h3 ADD_DATE='1686621554'>Test</h3>"
    processador = ObjetoTag(html_teste)
    tags = processador._extrair_tags()
    objeto_tag = processador._criar_objeto_tag(tags[0])
    assert objeto_tag.tag_name == "h3"
    assert objeto_tag.tag_text_content == "Test"
    assert "add_date" in objeto_tag.tag_atributos
