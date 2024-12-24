# tests/backend/models/test_bookmark_model.py

"""
Testes para o modelo do objeto Tag.
"""

import os
import sys
import json
from typing import Dict
from app.models.bookmark_model import ObjetoTag

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def criar_objeto_tag(html: str) -> ObjetoTag:
    """
    Cria uma instância de ObjetoTag para simplificar a inicialização nos testes.

    Args:
        html (str): HTML a ser processado.

    Returns:
        ObjetoTag: Instância inicializada.
    """
    return ObjetoTag(html)


def validar_tags(json_tags: str, esperadas: Dict[int, Dict[str, str]]):
    """
    Valida as tags extraídas contra os valores esperados.

    Args:
        json_tags (str): JSON com as tags extraídas.
        esperadas (Dict[int, Dict[str, str]]): Dicionário com os valores esperados.
    """
    tags = json.loads(json_tags)
    assert len(tags) == len(esperadas), "Quantidade de tags não corresponde"

    for idx, valores in esperadas.items():
        tag = tags[f"tag_{idx}"]
        for chave, valor in valores.items():
            assert tag[chave] == valor, f"Valor inesperado para {chave}: {tag[chave]} != {valor}"


def test_inicializacao_objeto_tag():
    """
    Verifica se o objeto ObjetoTag é inicializado corretamente.
    """
    html_teste = "<html><body><h3>Test</h3><a href='https://example.com'>Link</a></body></html>"
    objeto = criar_objeto_tag(html_teste)
    assert isinstance(objeto, ObjetoTag)


def test_extrair_tags():
    """
    Verifica se o método processar_tags retorna as tags corretas.
    """
    html_teste = "<html><body><h3>Teste</h3><a href='https://example.com'>Link</a></body></html>"
    objeto = criar_objeto_tag(html_teste)
    validar_tags(
        objeto.processar_tags(),
        {
            1: {"tag_name": "h3", "text_content": "Teste"},
            2: {"tag_name": "a", "text_content": "Link", "attributes": {"href": "https://example.com"}},
        },
    )


def test_extrair_tags_sem_relevantes():
    """
    Verifica se não retorna tags quando não há <h3> ou <a>.
    """
    html_teste = "<html><body><p>Sem tags relevantes</p></body></html>"
    objeto = criar_objeto_tag(html_teste)
    validar_tags(objeto.processar_tags(), {})


def test_processar_tags_variados():
    """
    Verifica o processamento de atributos e texto em tags variadas.
    """
    html_teste = """
    <html>
        <body>
            <h3 add_date="50123456789" last_modified="20123456789">Teste</h3>
            <a add_date="10123456789" href="https://example.com">Link</a>
        </body>
    </html>
    """
    objeto = criar_objeto_tag(html_teste)
    validar_tags(
        objeto.processar_tags(),
        {
            1: {
                "tag_name": "h3",
                "text_content": "Teste",
                "attributes": {"add_date": "50123456789", "last_modified": "20123456789"},
            },
            2: {
                "tag_name": "a",
                "text_content": "Link",
                "attributes": {"href": "https://example.com", "add_date": "10123456789"},
            },
        },
    )


def test_processar_tags_html_malformado():
    """
    Verifica se processar_tags lida com HTML malformado.
    """
    html_malformado = "<html><body><h3>Tag 1<p>Tag sem fechamento"
    objeto = criar_objeto_tag(html_malformado)
    assert objeto.processar_tags() != "{}", "JSON inesperadamente vazio"


def test_processar_tags_atributos_desconhecidos():
    """
    Verifica se atributos desconhecidos são processados corretamente.
    """
    html_teste = "<html><body><h3 unknown='value'>Test</h3></body></html>"
    objeto = criar_objeto_tag(html_teste)
    validar_tags(
        objeto.processar_tags(),
        {
            1: {
                "tag_name": "h3",
                "text_content": "Test",
                "attributes": {"unknown": "value"},
            }
        },
    )


def test_processar_tags_texto_em_branco():
    """
    Verifica se texto em branco ou espaços é tratado corretamente.
    """
    html_teste = "<html><body><h3>   </h3><a href='https://example.com'>   </a></body></html>"
    objeto = criar_objeto_tag(html_teste)
    validar_tags(
        objeto.processar_tags(),
        {
            1: {"tag_name": "h3", "text_content": ""},
            2: {"tag_name": "a", "text_content": "", "attributes": {"href": "https://example.com"}},
        },
    )
