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


from app.utils.conversores import ConversoresUtils

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

def test_converter_timestamp_tag_valid_string():
    """
    Verifica se um timestamp Unix válido, fornecido como string, é corretamente convertido
    para o formato legível de data e hora (DD/MM/YYYY HH:mm:ss).
    """
    conversores = ConversoresUtils()
    result = conversores.converter_timestamp_para_data_br("1686621554")
    assert result == "12/06/2023 22:59:14"

def test_converter_timestamp_tag_large_value():
    """
    Testa a conversão de um timestamp Unix muito grande (futuro distante).
    O objetivo é garantir que o método lida corretamente com valores fora do uso comum.
    """
    conversores = ConversoresUtils()
    result = conversores.converter_timestamp_para_data_br(9999999999)
    assert result == "20/11/2286 14:46:39"

def test_converter_tamanho_arquivo_invalid_type():
    """
    Garante que o método `converter_tamanho_arquivo` lança um TypeError
    ao receber um valor que não seja um número (int ou float).
    """
    conversores = ConversoresUtils()
    with pytest.raises(TypeError, match="O tamanho deve ser um número inteiro ou float."):
        conversores.converter_tamanho_arquivo("invalid")

def test_converter_tamanho_pasta_inexistente():
    """
    Verifica se uma exceção FileNotFoundError é lançada ao tentar calcular
    o tamanho de uma pasta inexistente.
    """
    conversores = ConversoresUtils()
    with pytest.raises(FileNotFoundError, match="A pasta '.*' não foi encontrada."):
        conversores.converter_tamanho_pasta("/caminho/inexistente")

def test_converter_tamanho_pasta_com_subdiretorios():
    """
    Testa o cálculo correto do tamanho total de uma pasta contendo
    subdiretórios e arquivos, incluindo arquivos em subníveis.
    """
    conversores = ConversoresUtils()
    with tempfile.TemporaryDirectory() as temp_dir:
        subdir = Path(temp_dir) / "subdir"
        subdir.mkdir()
        arquivo = subdir / "arquivo.txt"
        arquivo.write_bytes(b"a" * 1024)
        result = conversores.converter_tamanho_pasta(temp_dir)
        assert result == "1.00 KB"

def test_contar_arquivos_pasta_com_arquivos_ocultos():
    """
    Verifica se o método `contar_arquivos_pasta` conta corretamente
    arquivos visíveis e ocultos em um diretório.
    """
    conversores = ConversoresUtils()
    with tempfile.TemporaryDirectory() as temp_dir:
        Path(temp_dir, ".oculto.txt").write_text("Teste", encoding="utf-8")
        Path(temp_dir, "visivel.txt").write_text("Teste", encoding="utf-8")
        result = conversores.contar_arquivos_pasta(temp_dir)
        assert result == 2

def test_contar_links_html_aninhados():
    """
    Testa a contagem de links (<a>) em um documento HTML que contém
    links aninhados para garantir que todos são contabilizados corretamente.
    """
    html_com_links_aninhados = """
    <html>
        <body>
            <a href="https://example.com">Link 1 <span><a href="https://example.org">Link 2</a></span></a>
        </body>
    </html>
    """
    conversores = ConversoresUtils()
    result = conversores.contar_links_html(html_com_links_aninhados)
    assert result == 2

def test_extrair_titulo_html_multiplos_titulos():
    """
    Garante que o método `extrair_titulo_html` retorna o conteúdo do primeiro
    título (<title>) em um documento HTML com múltiplas tags <title>.
    """
    html_multiplos_titulos = """
    <html>
        <head>
            <title>Primeiro Título</title>
            <title>Segundo Título</title>
        </head>
    </html>
    """
    conversores = ConversoresUtils()
    result = conversores.extrair_titulo_html(html_multiplos_titulos)
    assert result == "Primeiro Título"

def test_extrair_titulo_html_caracteres_especiais():
    """
    Testa a extração de título em um documento HTML que contém caracteres
    especiais ou entidades HTML, garantindo a decodificação correta.
    """
    html_com_titulo_especial = """
    <html>
        <head>
            <title>Título &amp; Especial</title>
        </head>
    </html>
    """
    conversores = ConversoresUtils()
    result = conversores.extrair_titulo_html(html_com_titulo_especial)
    assert result == "Título & Especial"
