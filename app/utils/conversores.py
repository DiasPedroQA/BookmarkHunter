# app/utils/conversores.py

"""
Módulo de utilidades para conversão e manipulação de dados no projeto.

Este módulo oferece funções auxiliares para conversão de timestamps Unix para formatos legíveis, 
formatação de tamanhos de arquivos em unidades compreensíveis (como KB, MB, GB), 
e outras operações relacionadas a arquivos e dados em diversos formatos.

Funções incluídas:
- Conversão de timestamps Unix para o formato legível de data e hora (DD/MM/YYYY HH:mm:ss).
- Conversão de tamanhos de arquivos em bytes para unidades legíveis (B, KB, MB, GB, TB).
- Cálculo do tamanho total de uma pasta.
- Contagem de arquivos em diretórios e links em documentos HTML.
- Extração de título de documentos HTML.
- Contagem de chaves em arquivos JSON.

As funções deste módulo são projetadas para simplificar o processamento de dados no contexto de arquivos, 
diretórios e conteúdos de HTML/JSON.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict
from bs4 import BeautifulSoup


class ConversoresUtils:
    """
    Classe que fornece métodos para conversão de dados, como timestamps, tamanhos de arquivos,
    contagem de itens em pastas, e extração de informações de arquivos e HTML.
    """

    def converter_timestamp_tag(self, tag_timestamp: int | str) -> str:
        """
        Converte um timestamp Unix para o formato legível.

        Args:
            tag_timestamp (int | str): O timestamp Unix a ser convertido.

        Returns:
            str: O timestamp no formato "DD/MM/YYYY HH:mm:ss".

        Raises:
            ValueError: Se o timestamp não for um número válido.

        Exemplo:
            >>> utils = ConversoresUtils()
            >>> utils.converter_timestamp_tag(1686621554)
            '13/06/2023 15:25:54'
        """
        if tag_timestamp == "":
            return "Data não disponível"  # Ou algum valor padrão
        try:
            timestamp = int(tag_timestamp)
            return self._formatar_data(timestamp)
        except ValueError as exc:
            raise ValueError(
                "Timestamp inválido. Deve ser um inteiro ou string numérica."
            ) from exc

    def converter_timestamp_arquivo(
        self, timestamp_criacao_arquivo: float, timestamp_modificacao_arquivo: float
    ) -> Dict[str, str]:
        """
        Converte dois timestamps Unix para formatos legíveis.

        Args:
            timestamp_criacao_arquivo (float): Timestamp de criação do arquivo.
            timestamp_modificacao_arquivo (float): Timestamp de modificação do arquivo.

        Returns:
            dict: Dicionário com os timestamps convertidos nos formatos legíveis.

        Raises:
            ValueError: Se os timestamps forem inválidos.

        Exemplo:
            >>> utils = ConversoresUtils()
            >>> utils.converter_timestamp_arquivo(1686621554.0, 1686621600.0)
            {'timestamp_criacao': '13/06/2023 15:25:54', 'timestamp_modificacao': '13/06/2023 15:26:40'}
        """
        try:
            timestamp_criacao = float(timestamp_criacao_arquivo)
            timestamp_modificacao = float(timestamp_modificacao_arquivo)
            return {
                "timestamp_criacao": self._formatar_data(timestamp_criacao),
                "timestamp_modificacao": self._formatar_data(timestamp_modificacao),
            }
        except ValueError as exc:
            raise ValueError(
                "Timestamps inválidos. Devem ser números flutuantes válidos."
            ) from exc

    def converter_tamanho_arquivo(self, tamanho_bytes: int | float) -> str:
        """
        Converte o tamanho de um arquivo em bytes para uma unidade legível.

        Args:
            tamanho_bytes (int | float): Tamanho em bytes do arquivo.

        Returns:
            str: O tamanho formatado com a unidade apropriada (B, KB, MB, etc.).

        Raises:
            TypeError: Se o valor não for um número inteiro ou float.

        Exemplo:
            >>> utils = ConversoresUtils()
            >>> utils.converter_tamanho_arquivo(1024)
            '1.00 KB'
        """
        if not isinstance(tamanho_bytes, (int, float)):
            raise TypeError("O tamanho deve ser um número inteiro ou float.")
        return self._converter_tamanho_bytes(tamanho_bytes)

    def converter_tamanho_pasta(self, pasta_caminho: str) -> str:
        """
        Calcula e converte o tamanho total de uma pasta.

        Args:
            pasta_caminho (str): Caminho para a pasta.

        Returns:
            str: O tamanho total da pasta formatado com a unidade apropriada.

        Raises:
            FileNotFoundError: Se a pasta não for encontrada.
            ValueError: Se a pasta estiver vazia.
        """
        caminho = Path(pasta_caminho)
        if not caminho.is_dir():
            raise FileNotFoundError(f"A pasta '{pasta_caminho}' não foi encontrada.")
        tamanho_total = sum(f.stat().st_size for f in caminho.rglob("*") if f.is_file())
        if tamanho_total == 0:
            raise ValueError(f"A pasta '{pasta_caminho}' está vazia.")
        return self._converter_tamanho_bytes(tamanho_total)

    def contar_arquivos_pasta(self, pasta_caminho: str) -> int:
        """
        Conta a quantidade de arquivos dentro de uma pasta.

        Args:
            pasta_caminho (str): Caminho para a pasta.

        Returns:
            int: O número de arquivos na pasta.

        Raises:
            FileNotFoundError: Se a pasta não for encontrada.

        Exemplo:
            >>> utils = ConversoresUtils()
            >>> utils.contar_arquivos_pasta("/caminho/para/pasta")
            42
        """
        caminho = Path(pasta_caminho)
        if not caminho.is_dir():
            raise FileNotFoundError(f"A pasta '{pasta_caminho}' não foi encontrada.")
        return sum(1 for _ in caminho.rglob("*") if _.is_file())

    def contar_links_html(self, html_conteudo: str) -> int:
        """
        Conta o número de links (<a>) em um documento HTML.

        Args:
            html_conteudo (str): Conteúdo HTML como string.

        Returns:
            int: O número de tags <a> no HTML.

        Raises:
            ValueError: Se o HTML fornecido estiver vazio ou inválido.
        """
        if not html_conteudo.strip():
            raise ValueError("O conteúdo do HTML está vazio ou inválido.")
        soup = BeautifulSoup(html_conteudo, "html.parser")
        return len(soup.find_all("a"))

    def extrair_titulo_html(self, html_conteudo: str) -> str:
        """
        Extrai o conteúdo da tag <title> de um documento HTML.

        Args:
            html_conteudo (str): Conteúdo HTML como string.

        Returns:
            str: O conteúdo da tag <title> ou "Sem título" se não encontrado.

        Exemplo:
            >>> utils = ConversoresUtils()
            >>> html = "<html><head><title>Minha Página</title></head><body></body></html>"
            >>> utils.extrair_titulo_html(html)
            'Minha Página'
        """
        soup = BeautifulSoup(html_conteudo, "html.parser")
        return soup.title.string if soup.title else "Sem título"

    # Métodos utilitários (privados)

    @staticmethod
    def _formatar_data(timestamp: int) -> str:
        """
        Formata um timestamp Unix para o formato DD/MM/YYYY HH:mm:ss.

        Args:
            timestamp (int): O timestamp Unix.

        Returns:
            str: O timestamp formatado.

        Exemplo:
            >>> ConversoresUtils._formatar_data(1686621554)
            '13/06/2023 15:25:54'
        """
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def _converter_tamanho_bytes(tamanho: int | float) -> str:
        """
        Converte tamanhos em bytes para unidades legíveis.

        Args:
            tamanho (int | float): O tamanho em bytes.

        Returns:
            str: O tamanho formatado com a unidade apropriada.

        Raises:
            ValueError: Se o tamanho for negativo.
        """
        if tamanho < 0:
            raise ValueError("O tamanho em bytes não pode ser negativo.")
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if tamanho < 1024:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024
        return f"{tamanho:.2f} TB"


# # Exemplo de uso da classe ConversoresUtils  # pylint: disable=C0301

# # Criação de uma instância da classe ConversoresUtils
# conversores = ConversoresUtils()

# # Dados de exemplo para o uso da classe

# # HTML de exemplo
# HTML_EXEMPLO = """
# <!DOCTYPE NETSCAPE-Bookmark-file-1>
# <!--
#     This is an automatically generated file.
#     It will be read and overwritten. DO NOT EDIT!
# -->
# <html>
#     <head>
#         <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
#         <TITLE>Bookmarks</TITLE>
#     </head>
#     <body>
#         <H1>Bookmarks</H1>
#         <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#         <DL><p>
#             <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-2djh" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
#             <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
#         <DL><p>
#             <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
#     </body>
# </html>
# """

# # Timestamp inteiro de uso do objeto Tag para data de criação
# TIMESTAMP_CRIACAO = "1686621554"

# # Tamanho de arquivo em bytes
# TAMANHO_ARQUIVO = 1234567890

# # Caminho da pasta
# CAMINHO_PASTA = "/home/pedro-pm-dias/Downloads/"

# # Exemplos de uso dos métodos da classe ConversoresUtils

# # Converte timestamps para o formato legível
# timestamp_criacao_formatado = conversores.converter_timestamp_tag(TIMESTAMP_CRIACAO)
# print(f"Timestamp de criação formatado: {timestamp_criacao_formatado}")

# # Converte tamanho de arquivo
# tamanho_formatado = conversores.converter_tamanho_arquivo(TAMANHO_ARQUIVO)
# print(f"Tamanho do arquivo formatado: {tamanho_formatado}")

# # Converte tamanho de pasta
# tamanho_pasta_formatado = conversores.converter_tamanho_pasta(CAMINHO_PASTA)
# print(f"Tamanho da pasta formatado: {tamanho_pasta_formatado}")

# # Conta arquivos em uma pasta
# quantidade_arquivos = conversores.contar_arquivos_pasta(CAMINHO_PASTA)
# print(f"Quantidade de arquivos na pasta: {quantidade_arquivos}")

# # Conta links em HTML
# quantidade_links = conversores.contar_links_html(HTML_EXEMPLO)
# print(f"Quantidade de links no HTML: {quantidade_links}")

# # Extrai título de HTML
# titulo_html = conversores.extrair_titulo_html(HTML_EXEMPLO)
# print(f"Título extraído do HTML: {titulo_html}")
