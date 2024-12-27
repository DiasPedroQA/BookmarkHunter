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
import json
import pytest

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413, W0212, W0621
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app.models.bookmark_model import ObjetoTag


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


def test_instanciacao(html_teste: str) -> None:
    """
    Verifica se a classe ObjetoTag é instanciada corretamente com o HTML fornecido.

    Args:
        html_teste (str): HTML para teste.
    """
    processador = ObjetoTag(html=html_teste)
    assert processador.html == html_teste


def test_extracao_tags(html_teste: str) -> None:
    """
    Testa a extração de tags <h3> e <a> do HTML.

    Args:
        html_teste (str): HTML para teste.
    """
    processador = ObjetoTag(html=html_teste)
    tags = processador._extrair_tags()
    assert len(tags) == 4
    assert tags[0].name == "h3"
    assert tags[1].name == "a"


def test_processamento_atributos(html_teste: str):
    """
    Verifica o processamento e a conversão dos atributos das tags extraídas.

    Args:
        html_teste (str): HTML para teste.
    """
    processador = ObjetoTag(html=html_teste)
    tags = processador._extrair_tags()
    atributos_tag1 = processador._processar_atributos(tags[0])

    assert atributos_tag1["add_date"] == "12/06/2023 22:59:14"
    assert atributos_tag1["last_modified"] == "24/07/2024 09:13:55"


def test_processar_tags(html_teste: str):
    """
    Valida o processamento completo das tags em formato JSON.

    Args:
        html_teste (str): HTML para teste.
    """
    processador = ObjetoTag(html=html_teste)
    json_tags = processador.processar_tags()
    resultado_processado = json.loads(json_tags)

    assert resultado_processado["tag_1"]["tag_name"] == "<h3>"
    assert resultado_processado["tag_1"]["text_content"] == "Estudos"
    assert (
        resultado_processado["tag_1"]["attributes"]["add_date"] == "12/06/2023 22:59:14"
    )
    assert (
        resultado_processado["tag_4"]["attributes"]["href"]
        == "https://martinfowler.com/articles/practical-test-pyramid.html"
    )
