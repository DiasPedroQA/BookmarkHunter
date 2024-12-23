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
import json
from typing import Dict
from bs4 import BeautifulSoup


class ConversoresUtils:
    """
    Classe que fornece métodos para conversão de dados, como timestamps, tamanhos de arquivos,
    contagem de itens em pastas, e extração de informações de arquivos e HTML.
    """

    def __init__(self):
        pass

    # Métodos públicos

    def converter_timestamp_tag(self, tag_timestamp: str) -> str:
        """Converte um timestamp Unix para o formato DD/MM/YYYY HH:mm:ss."""
        return self._converter_timestamp(tag_timestamp)

    def converter_timestamps_arquivo(self, ctime: float, mtime: float) -> Dict[str, str]:
        """Converte timestamps de criação e modificação de arquivos para formato legível."""
        return {
            "data_criacao": self._formatar_data(ctime),
            "data_modificacao": self._formatar_data(mtime),
        }

    def converter_tamanho_arquivo(self, tamanho_arquivo: str) -> str:
        """Converte o tamanho de um arquivo em bytes para uma unidade legível."""
        return self._converter_tamanho_arquivo(tamanho_arquivo)

    def converter_tamanho_pasta(self, caminho_pasta: str) -> str:
        """Calcula e converte o tamanho total de uma pasta."""
        return self._converter_tamanho_pasta(caminho_pasta)

    def contar_arquivos_pasta(self, caminho_pasta: str) -> int:
        """Conta a quantidade de arquivos dentro de uma pasta."""
        return self._contar_arquivos_pasta(caminho_pasta)

    def contar_links_html(self, html: str) -> int:
        """Conta o número de links (<a>) em um documento HTML."""
        return self._contar_links_html(html)

    def extrair_titulo_html(self, html: str) -> str:
        """Extrai o conteúdo da tag <title> de um documento HTML."""
        return self._extrair_titulo_html(html)

    def contar_chaves_json(self, caminho_json: str) -> int:
        """Conta o número de chaves em um arquivo JSON."""
        return self._contar_chaves_json(caminho_json)

    # Métodos privados

    def _formatar_data(self, timestamp: float) -> str:
        """Formata um timestamp Unix para o formato DD/MM/YYYY HH:mm:ss"""
        try:
            return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
        except (ValueError, TypeError) as e:
            return f"Erro ao formatar data: {str(e)}"

    def _converter_timestamp(self, tag_timestamp: str) -> str:
        """Converte um timestamp Unix em formato string para o formato legível."""
        try:
            timestamp_int = int(tag_timestamp)
            return self._formatar_data(timestamp_int)
        except (ValueError, TypeError) as e:
            return f"Erro ao converter timestamp: {str(e)}"

    def _converter_tamanho_arquivo(self, tamanho_arquivo: str) -> str:
        """Converte o tamanho de arquivo em bytes para formato legível (KB, MB, GB, etc.)."""
        try:
            tamanho_arquivo = float(tamanho_arquivo)
            if tamanho_arquivo < 1024:
                return f"{tamanho_arquivo:.2f} B"
            elif tamanho_arquivo < 1024**2:
                return f"{tamanho_arquivo / 1024:.2f} KB"
            elif tamanho_arquivo < 1024**3:
                return f"{tamanho_arquivo / 1024**2:.2f} MB"
            elif tamanho_arquivo < 1024**4:
                return f"{tamanho_arquivo / 1024**3:.2f} GB"
            else:
                return f"{tamanho_arquivo / 1024**4:.2f} TB"
        except (ValueError, TypeError) as e:
            return f"Erro ao converter tamanho de arquivo: {str(e)}"

    def _converter_tamanho_pasta(self, caminho_pasta: str) -> str:
        """Calcula o tamanho total de uma pasta."""
        try:
            caminho_pasta = Path(caminho_pasta)
            tamanho_total = sum(f.stat().st_size for f in caminho_pasta.rglob('*') if f.is_file())
            return self._converter_tamanho_arquivo(str(tamanho_total))
        except (OSError, IOError) as e:
            return f"Erro ao calcular o tamanho da pasta: {str(e)}"

    def _contar_arquivos_pasta(self, caminho_pasta: str) -> int:
        """Conta a quantidade de arquivos em uma pasta."""
        try:
            caminho_pasta = Path(caminho_pasta)
            quantidade_arquivos = sum(1 for _ in caminho_pasta.rglob('*') if _.is_file())
            return quantidade_arquivos
        except FileNotFoundError:
            return f"A pasta '{caminho_pasta}' não foi encontrada."
        except PermissionError:
            return f"Permissão negada para acessar a pasta '{caminho_pasta}'."
        except OSError as e:
            return f"Erro no sistema de arquivos ao acessar a pasta '{caminho_pasta}': {str(e)}"
        except TypeError as e:
            return f"Erro inesperado ao contar os arquivos na pasta '{caminho_pasta}': {str(e)}"

    def _contar_links_html(self, html: str) -> int:
        """Conta o número de links (<a>) em um documento HTML."""
        try:
            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a")
            return len(links)
        except (AttributeError, ValueError) as e:
            return f"Erro ao contar links no HTML: {str(e)}"

    def _extrair_titulo_html(self, html: str) -> str:
        """Extrai o conteúdo da tag <title> de um documento HTML."""
        try:
            soup = BeautifulSoup(html, "html.parser")
            titulo = soup.title.string if soup.title else "Tag <title> não encontrada"
            return titulo
        except AttributeError:
            return "Erro ao acessar a tag <title> no HTML."
        except ValueError as e:
            return f"Erro ao processar o HTML: {str(e)}"
        except TypeError as e:
            return f"Erro inesperado ao extrair o título do HTML: {str(e)}"

    def _contar_chaves_json(self, caminho_json: str) -> int:
        """Conta o número de chaves em um arquivo JSON."""
        try:
            with open(caminho_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return len(dados)
        except (IOError, json.JSONDecodeError) as e:
            return f"Erro ao contar chaves no JSON: {str(e)}"


# Exemplo de uso da classe ConversoresUtils

# HTML de exemplo  # pylint: disable=C0301
# HTML = """
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

# Criação de uma instância da classe ConversoresUtils
# conversores = ConversoresUtils()

# Exemplo de conversão de timestamps
# TIMESTAMP_CRIACAO = "1686621554"  # Timestamp UNIX de exemplo
# TIMESTAMP_MODIFICACAO = "1721823235"  # Timestamp UNIX de exemplo

# Convertendo timestamps para o formato legível
# timestamp_criacao_formatado = conversores.converter_timestamp_tag(TIMESTAMP_CRIACAO)
# timestamp_modificacao_formatado = conversores.converter_timestamp_tag(TIMESTAMP_MODIFICACAO)

# print(f"Data de criação: {timestamp_criacao_formatado}")
# print(f"Data de modificação: {timestamp_modificacao_formatado}")

# Exemplo de contagem de links no HTML
# numero_links = conversores.contar_links_html(HTML)
# print(f"Número de links no HTML: {numero_links}")

# Exemplo de extração do título do HTML
# titulo_html = conversores.extrair_titulo_html(HTML)
# print(f"Título do HTML: {titulo_html}")
