# app/models/bookmark_model.py


"""
Módulo para processar tags HTML e extrair informações relevantes.
Este módulo fornece a classe TagProcessor para extrair e formatar dados de tags <h3> e <a> em documentos HTML.

Classes:
    TagProcessor: Processa tags HTML e converte os dados extraídos em JSON.

Exemplo de uso:
    html = '''<html><body><h3>Título</h3><a href="https://example.com">Link</a></body></html>'''
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    print(resultado)
"""

import sys
import os
from typing import Dict
import json
from bs4 import BeautifulSoup, Tag, ResultSet
from app.utils.conversores import formatar_timestamp
from app.utils.geradores import gerar_id

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../../')))


class TagProcessor:
    """
    Classe para processar tags HTML e extrair informações relevantes.

    Args:
        html (str): O HTML a ser processado.

    Atributos:
        html (str): O HTML fornecido para processamento.
        tags (ResultSet[Tag]): Conjunto de tags extraídas do HTML.

    Métodos:
        processar_tags: Processa todas as tags extraídas e retorna os dados em JSON.
    """

    def __init__(self, html: str):
        """
        Inicializa a classe com o HTML fornecido e extrai as tags relevantes.

        Args:
            html (str): O conteúdo HTML a ser processado.
        """
        self.html = html
        self.tags: ResultSet[Tag] = self._extrair_tags()

    def _extrair_tags(self) -> ResultSet[Tag]:
        """
        Extrai tags <a> e <h3> do HTML usando BeautifulSoup.

        Returns:
            ResultSet[Tag]: Uma lista de objetos Tag contendo as tags extraídas.
        """
        soup = BeautifulSoup(self.html, "html.parser")
        return soup.find_all(["h3", "a"])

    def _processar_tag(self, tag: Tag) -> Dict[str, str]:
        """
        Processa uma tag específica e retorna os dados formatados.

        Args:
            tag (Tag): A tag HTML a ser processada.

        Returns:
            Dict[str, str]: Um dicionário com os dados processados da tag.
        """
        tag_attrs = {chave.lower(): valor for chave, valor in tag.attrs.items()}
        tag_data = {
            "id": gerar_id(),
            "tag_name": f"<{tag.name}>",
            "text_content": tag.text.strip(),
            "add_date": formatar_timestamp(tag_attrs.get("add_date", "")),
        }

        if tag.name == "h3":
            tag_data["last_modified"] = formatar_timestamp(tag_attrs.get("last_modified", ""))
        elif tag.name == "a":
            tag_data["href"] = tag_attrs.get("href", None)

        return {chave: valor for chave, valor in tag_data.items() if valor}

    def processar_tags(self) -> str:
        """
        Processa todas as tags extraídas e retorna os dados em formato JSON.

        Returns:
            str: Um JSON com as informações processadas das tags.
        """
        resultado = {
            f"tag_{idx + 1}": self._processar_tag(tag)
            for idx, tag in enumerate(self.tags)
        }
        return json.dumps(resultado, indent=4, ensure_ascii=False)


# if __name__ == "__main__":
#     # Exemplo de uso com HTML de teste
#     # pylint: disable=C0301
#     HTML_TESTE = """
#     <html>
#         <body>
#             <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#         <DL><p>
#             <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702">[pt-BR] Fundamentos do Git</A>
#             <DT><H3 ADD_DATE="1618539876" LAST_MODIFIED="1686055731">Python</H3>
#         <DL><p>
#             <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793">A Pirâmide do Teste Prático</A>
#         </body>
#     </html>
#     """

#     processador = TagProcessor(html=HTML_TESTE)
#     resultado_processado = processador.processar_tags()
#     print(resultado_processado)
