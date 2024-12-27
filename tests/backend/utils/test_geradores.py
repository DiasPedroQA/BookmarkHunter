# tests/backend/utils/geradores.py

"""
Este módulo contém um conjunto de testes para a classe `GeradoresUtils`, localizada no
módulo `app.utils.geradores`. A classe `GeradoresUtils` fornece métodos utilitários para a
criação e manipulação de arquivos simulados e conteúdo HTML em memória, como a criação
de arquivos, pastas e tags HTML personalizadas.

Os testes são implementados utilizando o framework `pytest` e cobrem os seguintes cenários:

1. **Geração de IDs únicos**:
   - Testa a função `gerar_id` para garantir que ela retorne IDs únicos a cada chamada.

2. **Criação de arquivos simulados**:
   - Testa a função `criar_arquivo`, verificando se os arquivos são armazenados corretamente
     no dicionário `arquivos_simulados` com o nome e conteúdo fornecidos.

3. **Criação de pastas simuladas**:
   - Testa a função `criar_pasta`, garantindo que as pastas sejam armazenadas corretamente
     no dicionário `pastas_simuladas` com o nome correto.

4. **Criação de tags HTML**:
   - Testa a função `criar_tag_html`, garantindo que tags HTML sejam geradas corretamente
     com o conteúdo e atributos fornecidos.
   - Testa a função `criar_arquivo_html`, que gera um arquivo HTML com múltiplas tags.

5. **Casos de erro e validações**:
   - Testa o comportamento da função `criar_elemento` quando um tipo de elemento inválido é passado.
   - Testa a criação de tags HTML sem atributos e com conteúdo vazio.
   - Testa a criação de arquivos e pastas com conteúdo ou nome vazio.

Esses testes garantem que os métodos da classe `GeradoresUtils` funcionem corretamente,
lidando com diferentes entradas e cenários de uso, incluindo casos de erro esperados.

Requisitos:
    - O framework `pytest` deve estar instalado.
    - O módulo `app.utils.geradores` deve estar disponível e a classe `GeradoresUtils` corretamente implementada.

Exemplo de execução dos testes:
    Para rodar todos os testes, basta executar o comando `pytest` no diretório raiz do projeto.

"""

import os
import sys
import pytest
from app.utils.geradores import GeradoresUtils


# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


# Teste de geração de ID único
def test_gerar_id_unico():
    """
    Testa a geração de IDs únicos. O objetivo é garantir que a função `gerar_id`
    retorne IDs diferentes a cada chamada.
    """
    gerador = GeradoresUtils()
    id1 = gerador.gerar_id()
    id2 = gerador.gerar_id()
    assert id1 != id2  # Verifica se os IDs gerados são diferentes

# Teste de criação de arquivo
def test_criar_arquivo():
    """
    Testa a função `criar_arquivo`, verificando se o arquivo é armazenado corretamente
    no dicionário `arquivos_simulados` com o nome e conteúdo corretos.
    """
    gerador = GeradoresUtils()
    arquivo_id = gerador.criar_arquivo("arquivo_teste.txt", "Conteúdo do arquivo")
    assert arquivo_id in gerador.arquivos_simulados  # Verifica se o ID do arquivo foi adicionado
    assert gerador.arquivos_simulados[arquivo_id]["nome_arquivo"] == "arquivo_teste.txt"  # Verifica o nome do arquivo
    assert gerador.arquivos_simulados[arquivo_id]["conteudo"] == "Conteúdo do arquivo"  # Verifica o conteúdo do arquivo

# Teste de criação de pasta
def test_criar_pasta():
    """
    Testa a função `criar_pasta`, garantindo que a pasta seja corretamente armazenada
    no dicionário `pastas_simuladas` com o nome correto.
    """
    gerador = GeradoresUtils()
    pasta_id = gerador.criar_pasta("pasta_teste")
    assert pasta_id in gerador.pastas_simuladas  # Verifica se a pasta foi criada e armazenada
    assert gerador.pastas_simuladas[pasta_id]["nome_pasta"] == "pasta_teste"  # Verifica o nome da pasta

# Teste de criação de tag HTML
def test_criar_tag_html():
    """
    Testa a criação de uma tag HTML utilizando a função `criar_tag_html`.
    A função deve adicionar corretamente a tag à estrutura HTML com os atributos fornecidos.
    """
    gerador = GeradoresUtils()
    html_resultado = gerador.criar_tag_html("div", "Conteúdo da div", {"class": "classe-teste"})
    # Verifica se a tag HTML gerada contém o conteúdo e os atributos corretos
    assert '<div class="classe-teste">Conteúdo da div</div>' in html_resultado

# Teste de criação de arquivo HTML com várias tags
def test_criar_arquivo_html():
    """
    Testa a criação de um arquivo HTML com múltiplas tags. A função `criar_arquivo_html`
    deve gerar um HTML válido com base em uma lista de dicionários contendo as tags,
    conteúdo e atributos.
    """
    gerador = GeradoresUtils()
    dados_html = [
        {"tag": "h1", "conteudo": "Título", "atributos": {}},
        {"tag": "p", "conteudo": "Um parágrafo.", "atributos": {}}
    ]
    html_gerado = gerador.criar_arquivo_html(dados_html)
    # Verifica se as tags HTML geradas estão no HTML final
    assert "<h1>Título</h1>" in html_gerado
    assert "<p>Um parágrafo.</p>" in html_gerado

# Teste de criação de elemento inválido
def test_criar_elemento_invalido():
    """
    Testa o comportamento da função `criar_elemento` quando um tipo de elemento inválido
    é passado. A função deve lançar um erro do tipo `ValueError`.
    """
    gerador = GeradoresUtils()
    with pytest.raises(ValueError, match="Tipo 'invalido' não suportado."):
        gerador.criar_elemento("invalido", "nome")  # Tenta criar um elemento com tipo inválido

# Teste de criação de tag HTML sem atributos
def test_criar_tag_html_sem_atributos():
    """
    Testa a criação de uma tag HTML sem atributos. A função `criar_tag_html` deve
    gerar uma tag HTML simples com o conteúdo fornecido.
    """
    gerador = GeradoresUtils()
    html_resultado = gerador.criar_tag_html("span", "Texto sem atributos")
    # Verifica se a tag HTML gerada contém o conteúdo correto
    assert '<span>Texto sem atributos</span>' in html_resultado

# Teste de criação de arquivo com conteúdo vazio
def test_criar_arquivo_com_conteudo_vazio():
    """
    Testa a criação de um arquivo com conteúdo vazio. A função `criar_arquivo` deve
    ser capaz de criar arquivos mesmo que o conteúdo esteja vazio.
    """
    gerador = GeradoresUtils()
    arquivo_id = gerador.criar_arquivo("arquivo_vazio.txt", "")
    # Verifica se o arquivo foi criado corretamente com conteúdo vazio
    assert arquivo_id in gerador.arquivos_simulados
    assert gerador.arquivos_simulados[arquivo_id]["conteudo"] == ""

# Teste de criação de pasta com nome vazio
def test_criar_pasta_com_nome_vazio():
    """
    Testa a criação de uma pasta com nome vazio. A função `criar_pasta` deve
    ser capaz de criar uma pasta mesmo com um nome vazio.
    """
    gerador = GeradoresUtils()
    pasta_id = gerador.criar_pasta("")
    # Verifica se a pasta foi criada corretamente com um nome vazio
    assert pasta_id in gerador.pastas_simuladas
    assert gerador.pastas_simuladas[pasta_id]["nome_pasta"] == ""

# Teste de criação de arquivo HTML com tags vazias
def test_criar_arquivo_html_com_tags_vazias():
    """
    Testa a criação de um arquivo HTML contendo tags vazias. Mesmo que o conteúdo
    das tags esteja vazio, a função `criar_arquivo_html` deve gerar as tags corretamente.
    """
    gerador = GeradoresUtils()
    dados_html = [
        {"tag": "h2", "conteudo": "", "atributos": {}},
        {"tag": "a", "conteudo": "", "atributos": {"href": "#"}}
    ]
    html_gerado = gerador.criar_arquivo_html(dados_html)
    # Verifica se as tags vazias são geradas corretamente
    assert "<h2></h2>" in html_gerado
    assert '<a href="#">' in html_gerado
