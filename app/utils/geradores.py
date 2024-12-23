# app/utils/geradores.py

"""
Arquivo de utilidades para geração de dados úteis para o projeto.
"""

import hashlib
import time
from typing import Optional
from bs4 import BeautifulSoup


class Geradores:
    """
    A classe `Geradores` fornece um conjunto de métodos utilitários para gerar
    e gerenciar arquivos simulados, pastas e conteúdo HTML em memória.
    Ela foi projetada para ser usada como uma classe auxiliar dentro de uma aplicação maior.
    
    O método `__init__` inicializa a classe com armazenamento em memória para arquivos simulados,
    pastas e conteúdo HTML.
    O método `gerar_id` gera um ID único utilizando um hash MD5 do timestamp atual.
    Os métodos `criar_arquivo`, `ler_arquivo`, `atualizar_arquivo` e `deletar_arquivo` fornecem
    funcionalidades para criar, ler, atualizar e deletar arquivos simulados, respectivamente.
    Os métodos `criar_pasta`, `listar_arquivos_pasta`, `adicionar_arquivo_pasta` e `remover_arquivo_pasta`
    fornecem funcionalidades para criar, listar, adicionar e remover arquivos de pastas simuladas.
    Os métodos `criar_tag_html`, `ler_tag_html`, `atualizar_tag_html` e `deletar_tag_html` fornecem
    funcionalidades para criar, ler, atualizar e deletar tags HTML no conteúdo HTML simulado.
    """
    def __init__(self):
        """
        Inicializa a classe Geradores com armazenamento simulado para arquivos,
        pastas e HTML.
        """
        self.arquivos_simulados = {}  # Simulação de arquivo em memória
        self.pastas_simuladas = {}  # Simulação de pastas em memória
        self.html_teste = """
            <html>
                <body>
                    <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
                <DL><p>
                <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
                    <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
                <DL><p>
                <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
                </body>
            </html>"""  # Simulação de HTML em memória

    def gerar_id(self) -> str:
        """
        Gera um ID único utilizando o hash MD5 baseado no timestamp atual.
        
        :return: Um ID único gerado em formato hexadecimal.
        """
        return hashlib.md5(str(time.time()).encode()).hexdigest()

    def criar_arquivo(self, nome: str, conteudo: str) -> str:
        """
        Cria um arquivo simulado com o conteúdo fornecido e retorna um ID único
        para o arquivo.

        :param nome: Nome do arquivo.
        :param conteudo: Conteúdo que será escrito no arquivo.
        :return: ID único gerado para o arquivo.
        """
        arquivo_id = hashlib.md5(nome.encode()).hexdigest()
        self.arquivos_simulados[arquivo_id] = conteudo
        return arquivo_id

    def ler_arquivo(self, arquivo_id: str) -> Optional[str]:
        """
        Lê o conteúdo de um arquivo simulado usando seu ID.

        :param arquivo_id: ID único do arquivo a ser lido.
        :return: Conteúdo do arquivo ou None se o arquivo não existir.
        """
        return self.arquivos_simulados.get(arquivo_id)

    def atualizar_arquivo(self, arquivo_id: str, novo_conteudo: str) -> bool:
        """
        Atualiza o conteúdo de um arquivo simulado existente.

        :param arquivo_id: ID único do arquivo a ser atualizado.
        :param novo_conteudo: Novo conteúdo a ser escrito no arquivo.
        :return: True se o arquivo foi atualizado, False se o arquivo não foi encontrado.
        """
        if arquivo_id in self.arquivos_simulados:
            self.arquivos_simulados[arquivo_id] = novo_conteudo
            return True
        return False

    def deletar_arquivo(self, arquivo_id: str) -> bool:
        """
        Deleta um arquivo simulado.

        :param arquivo_id: ID único do arquivo a ser deletado.
        :return: True se o arquivo foi deletado, False se o arquivo não foi encontrado.
        """
        if arquivo_id in self.arquivos_simulados:
            del self.arquivos_simulados[arquivo_id]
            return True
        return False

    def criar_pasta(self, nome: str) -> str:
        """
        Cria uma pasta simulada.

        :param nome: Nome da pasta a ser criada.
        :return: ID único gerado para a pasta.
        """
        pasta_id = hashlib.md5(nome.encode()).hexdigest()
        self.pastas_simuladas[pasta_id] = []
        return pasta_id

    def listar_arquivos_pasta(self, pasta_id: str) -> Optional[list]:
        """
        Lista os arquivos presentes em uma pasta simulada.

        :param pasta_id: ID único da pasta a ser consultada.
        :return: Lista de IDs de arquivos na pasta ou None se a pasta não existir.
        """
        return self.pastas_simuladas.get(pasta_id)

    def adicionar_arquivo_pasta(self, pasta_id: str, arquivo_id: str) -> bool:
        """
        Adiciona um arquivo simulado a uma pasta simulada.

        :param pasta_id: ID único da pasta.
        :param arquivo_id: ID único do arquivo a ser adicionado.
        :return: True se o arquivo foi adicionado à pasta, False se a pasta não existir.
        """
        if pasta_id in self.pastas_simuladas:
            self.pastas_simuladas[pasta_id].append(arquivo_id)
            return True
        return False

    def remover_arquivo_pasta(self, pasta_id: str, arquivo_id: str) -> bool:
        """
        Remove um arquivo simulado de uma pasta simulada.

        :param pasta_id: ID único da pasta.
        :param arquivo_id: ID único do arquivo a ser removido.
        :return: True se o arquivo foi removido da pasta, False se a pasta ou o arquivo não existirem.
        """
        if pasta_id in self.pastas_simuladas and arquivo_id in self.pastas_simuladas[pasta_id]:
            self.pastas_simuladas[pasta_id].remove(arquivo_id)
            return True
        return False

    def criar_tag_html(self, tag: str, conteudo: str, atributos: Optional[dict] = None) -> str:
        """
        Cria uma nova tag HTML com o conteúdo e atributos fornecidos e a adiciona ao HTML simulado.

        :param tag: Tipo da tag HTML a ser criada (ex: 'a', 'div', 'h1').
        :param conteudo: Conteúdo a ser inserido dentro da tag HTML.
        :param atributos: Atributos opcionais a serem adicionados à tag HTML.
        :return: O HTML atualizado com a nova tag.
        """
        soup = BeautifulSoup(self.html_teste, "html.parser")
        nova_tag = soup.new_tag(tag, **(atributos or {}))
        nova_tag.string = conteudo
        soup.body.append(nova_tag)
        return str(soup)

    def ler_tag_html(self, tag: str) -> Optional[str]:
        """
        Lê o conteúdo de uma tag HTML específica no HTML simulado.

        :param tag: Tipo da tag HTML a ser lida (ex: 'a', 'h1').
        :return: Conteúdo da tag HTML ou None se a tag não for encontrada.
        """
        soup = BeautifulSoup(self.html_teste, "html.parser")
        tag_encontrada = soup.find(tag)
        return tag_encontrada.string if tag_encontrada else None

    def atualizar_tag_html(self, tag: str, novo_conteudo: str) -> bool:
        """
        Atualiza o conteúdo de uma tag HTML existente no HTML simulado.

        :param tag: Tipo da tag HTML a ser atualizada (ex: 'a', 'h1').
        :param novo_conteudo: Novo conteúdo a ser inserido na tag HTML.
        :return: True se a tag foi atualizada, False se a tag não foi encontrada.
        """
        soup = BeautifulSoup(self.html_teste, "html.parser")
        tag_encontrada = soup.find(tag)
        if tag_encontrada:
            tag_encontrada.string = novo_conteudo
            return True
        return False

    def deletar_tag_html(self, tag: str) -> bool:
        """
        Deleta uma tag HTML específica do HTML simulado.

        :param tag: Tipo da tag HTML a ser deletada (ex: 'a', 'h1').
        :return: True se a tag foi deletada, False se a tag não foi encontrada.
        """
        soup = BeautifulSoup(self.html_teste, "html.parser")
        tag_encontrada = soup.find(tag)
        if tag_encontrada:
            tag_encontrada.decompose()
            return True
        return False
