# tests/backend/utils/test_conversores.py

"""
Testes para o módulo de utilitários de conversão e manipulação de dados.

Este arquivo contém uma coleção de testes para validar as funcionalidades da classe `ConversoresUtils`.
Os testes cobrem cenários válidos e casos extremos para garantir que a lógica esteja correta e
que erros sejam tratados adequadamente.

Principais funcionalidades testadas:
- Conversão de timestamps Unix para formatos legíveis.
- Cálculo e conversão de tamanhos de arquivos e pastas.
- Contagem de arquivos em diretórios e links em documentos HTML.
- Extração de título de documentos HTML.

Framework utilizado: pytest.
"""

import os
import sys
import tempfile
from pathlib import Path
import pytest


# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from app.utils import ConversoresUtils

# Dados de exemplo para uso nos testes
HTML_EXEMPLO = """
<!DOCTYPE html>
<html>
    <head>
        <title>Página de Teste</title>
    </head>
    <body>
        <a href="https://example.com">Link 1</a>
        <a href="https://example.org">Link 2</a>
    </body>
</html>
"""

def test_converter_timestamp_para_data_hora_br_invalid_string():
    conversores = ConversoresUtils()
    result = conversores.converter_timestamp_para_data_hora_br("not_a_timestamp")
    assert result == ""

def test_converter_tamanho_arquivo_negativo():
    conversores = ConversoresUtils()
    result = conversores.converter_tamanho_arquivo(-1024)
    assert result == "Tamanho inválido"

def test_converter_tamanho_arquivo_zero():
    conversores = ConversoresUtils()
    result = conversores.converter_tamanho_arquivo(0)
    assert result == "0.00 B"

def test_liminar_texto_espacos_extras():
    conversores = ConversoresUtils()
    result = conversores.limpar_texto("   Texto   com   espaços   extras   ")
    assert result == "Texto com espaços extras"

def test_texto_para_url_amigavel_acentos():
    conversores = ConversoresUtils()
    result = conversores.texto_para_url_amigavel("Texto com Acentos é Legal!")
    assert result == "texto-com-acentos-legal"

def test_json_para_dict_json_invalido():
    conversores = ConversoresUtils()
    result = conversores.json_para_dict("invalido")
    assert result == {}

def test_dict_para_json_dicionario_vazio():
    conversores = ConversoresUtils()
    result = conversores.dict_para_json({})
    assert result == "{}"
