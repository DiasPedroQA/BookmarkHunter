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


class ConversoresUtils:
    """
    Classe que fornece métodos para conversão de dados, como timestamps, tamanhos de arquivos,
    contagem de itens em pastas.
    """

    def converter_timestamp_para_data_br(self, tag_timestamp: int | str) -> str:
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
            >>> utils.converter_timestamp_para_data_br(1686621554)
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
# if __name__ == "__main__":
#     # Criação de uma instância da classe ConversoresUtils
#     conversores = ConversoresUtils()

#     # Dados de exemplo para o uso da classe

#     # HTML de exemplo
#     HTML_EXEMPLO = """
#     <!DOCTYPE NETSCAPE-Bookmark-file-1>
#     <!-- This is an automatically generated file. It will be read and overwritten. DO NOT EDIT! -->
#     <html>
#         <head>
#             <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
#             <TITLE>Bookmarks</TITLE>
#         </head>
#         <body>
#             <H1>Bookmarks</H1>
#             <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#             <DL><p>
#                 <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-2djh" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
#                 <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
#             <DL><p>
#                 <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
#         </body>
#     </html>
#     """
#     # Exemplos de uso das funções

#     # Converte timestamp para data formatada
#     timestamp_formatado = conversores.converter_timestamp_para_data_br(1686621554)
#     print(f"Timestamp formatado: {timestamp_formatado}")

#     # Converte tamanho de arquivo para unidade legível
#     tamanho_formatado = conversores.converter_tamanho_arquivo(1234567890)
#     print(f"Tamanho do arquivo formatado: {tamanho_formatado}")

#     # Conta arquivos em uma pasta
#     quantidade_arquivos = conversores.contar_arquivos_pasta("/home/pedro-pm-dias/Downloads/Chrome")
#     print(f"Quantidade de arquivos na pasta: {quantidade_arquivos}")
