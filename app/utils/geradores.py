# app/utils/geradores.py

"""
Módulo com a classe `GeradoresUtils` que oferece métodos para criar e
manipular arquivos simulados e conteúdo HTML em memória.
A classe permite gerar IDs únicos, criar e manipular arquivos e
pastas simuladas, e gerar tags HTML com atributos personalizados.

Métodos principais:
- Gerar IDs únicos com base no timestamp.
- Criar, ler, atualizar e deletar arquivos e pastas simuladas.
- Criar e manipular tags HTML com atributos personalizados.

Exemplo de uso:
    gerador = GeradoresUtils()
    id_arquivo = gerador.criar_arquivo('teste.txt', 'Conteúdo do arquivo')
    html_atualizado = gerador.criar_tag_html('p', 'Texto de parágrafo', {'class': 'paragrafo'})
"""

import hashlib
import time
from typing import Optional, List, Dict
from bs4 import BeautifulSoup


class GeradoresUtils:
    """
    A classe `GeradoresUtils` fornece métodos utilitários para a criação e manipulação
    de arquivos simulados e conteúdo HTML em memória. Ela facilita a criação de
    tags HTML com atributos específicos e a manipulação de arquivos simulados.
    """

    def __init__(self):
        """
        Inicializa a classe GeradoresUtils com armazenamento em memória para arquivos,
        pastas e conteúdo HTML.
        """
        self.arquivos_simulados = {}  # Dicionário para armazenar arquivos simulados
        self.pastas_simuladas = {}  # Dicionário para armazenar pastas simuladas
        self.html_base = """<html><body></body></html>"""  # HTML base simulado

    def gerar_id(self) -> str:
        """
        Gera um ID único utilizando um hash MD5 baseado no timestamp atual.

        :return: Um ID único gerado em formato hexadecimal.
        """
        return hashlib.md5(str(time.time()).encode()).hexdigest()

    def criar_elemento(
        self,
        tipo: str,
        nome: str,
        conteudo: Optional[str] = None,
        atributos: Optional[dict] = None,
    ) -> str:
        """
        Cria um novo elemento (arquivo, pasta ou tag HTML) dependendo do tipo especificado.

        :param tipo: Tipo de elemento a ser criado, pode ser 'html', 'arquivo' ou 'pasta'.
        :param nome: Nome do elemento (nome do arquivo ou nome da tag HTML).
        :param conteudo: Conteúdo a ser inserido no elemento (opcional).
        :param atributos: Atributos a serem adicionados à tag HTML (somente para tipo 'html').
        :return: ID único do elemento ou HTML atualizado.
        """
        if tipo == "html":
            return self.criar_tag_html(nome, conteudo, atributos)
        if tipo == "arquivo":
            return self.criar_arquivo(nome, conteudo)
        if tipo == "pasta":
            return self.criar_pasta(nome)
        raise ValueError(f"Tipo '{tipo}' não suportado.")

    def criar_tag_html(
        self, tag: str, conteudo: str, atributos: Optional[dict] = None
    ) -> str:
        """
        Cria uma nova tag HTML com o conteúdo e atributos fornecidos.

        :param tag: Tipo da tag HTML a ser criada (ex: 'a', 'div', 'h1').
        :param conteudo: Conteúdo a ser inserido dentro da tag HTML.
        :param atributos: Atributos opcionais a serem adicionados à tag HTML.
        :return: O HTML atualizado com a nova tag.
        """
        soup = BeautifulSoup(self.html_base, "html.parser")
        nova_tag = soup.new_tag(tag, **(atributos or {}))
        nova_tag.string = conteudo
        soup.body.append(nova_tag)
        return str(soup)

    def criar_arquivo(self, nome_arquivo: str, conteudo: str) -> str:
        """
        Cria um arquivo simulado com o conteúdo fornecido e retorna um ID único
        para o arquivo.

        :param nome_arquivo: Nome do arquivo a ser criado.
        :param conteudo: Conteúdo que será escrito no arquivo.
        :return: ID único gerado para o arquivo.
        """
        arquivo_id = self.gerar_id()
        self.arquivos_simulados[arquivo_id] = {
            "nome_arquivo": nome_arquivo,
            "conteudo": conteudo,
        }
        return arquivo_id

    def criar_pasta(self, nome_pasta: str) -> str:
        """
        Cria uma pasta simulada.

        :param nome_pasta: Nome da pasta a ser criada.
        :return: ID único gerado para a pasta.
        """
        pasta_id = self.gerar_id()
        self.pastas_simuladas[pasta_id] = {"nome_pasta": nome_pasta, "arquivos": []}
        return pasta_id

    def criar_arquivo_html(self, dados: List[Dict[str, Optional[str]]]) -> str:
        """
        Cria um arquivo HTML estruturado com base nos dados fornecidos.
        Cada entrada no 'dados' deve ser um dicionário com as chaves correspondentes
        aos atributos da tag HTML e seus respectivos valores.

        Exemplo de dados:
        [
            {"tag": "h3", "conteudo": "Estudos",
            "atributos": {"ADD_DATE": "1686621554", "LAST_MODIFIED": "1721823235"}},
            {"tag": "a", "conteudo": "[pt-BR] Fundamentos do Git",
            "atributos": {"HREF": "https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh",
            "ADD_DATE": "1686055702"}}
        ]

        :param dados: Lista de dicionários contendo as tags, conteúdo e atributos.
        :return: O HTML completo gerado.
        """
        soup = BeautifulSoup("<html><body></body></html>", "html.parser")

        for item in dados:
            tag = item.get("tag")
            conteudo = item.get("conteudo")
            atributos = item.get("atributos", {})
            nova_tag = soup.new_tag(tag, **atributos)
            nova_tag.string = conteudo
            soup.body.append(nova_tag)

        return str(soup)


### Exemplo de Uso:

if __name__ == "__main__":
    # Inicializando a classe GeradoresUtils
    gerador = GeradoresUtils()

    # Criar e manipular arquivos simulados
    print("### Criando Arquivos e Pastas ###")

    # Criar arquivo
    ID_ARQUIVO = gerador.criar_arquivo("arquivo1.txt", "Conteúdo do arquivo 1")
    print(f"Arquivo criado com ID: {ID_ARQUIVO}")

    # Criar pasta
    ID_PASTA = gerador.criar_pasta("pasta1")
    print(f"Pasta criada com ID: {ID_PASTA}")

    print("\n### Criando Tags HTML ###")

    # Criar uma tag HTML simples
    HTML_ATUALIZADO = gerador.criar_tag_html(
        "p", "Este é um parágrafo.", {"class": "paragrafo"}
    )
    print(f"HTML Atualizado com tag 'p': {HTML_ATUALIZADO}")

    print("\n### Criando Arquivo HTML com múltiplas tags ###")

    # Criando tags HTML com atributos separados
    dados_html = [
        {
            "tag": "h3",
            "conteudo": "Estudos",
            "atributos": {"ADD_DATE": "1686621554", "LAST_MODIFIED": "1721823235"},
        },
        {
            "tag": "a",
            "conteudo": "[pt-BR] Fundamentos do Git",
            "atributos": {
                "HREF": "https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh",
                "ADD_DATE": "1686055702",
            },
        },
        {
            "tag": "h3",
            "conteudo": "Python",
            "atributos": {"ADD_DATE": "1618539876", "LAST_MODIFIED": "1686055731"},
        },
        {
            "tag": "a",
            "conteudo": "A Pirâmide do Teste Prático",
            "atributos": {
                "HREF": "https://martinfowler.com/articles/practical-test-pyramid.html",
                "ADD_DATE": "1691737793",
            },
        },
    ]

    # Criar o arquivo HTML com múltiplas tags
    HTML_GERADO = gerador.criar_arquivo_html(dados_html)
    print(f"HTML Completo Gerado:\n{HTML_GERADO}")
