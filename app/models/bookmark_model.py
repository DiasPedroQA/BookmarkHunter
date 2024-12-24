# app/models/bookmark_model.py

"""
Módulo para processar tags HTML e extrair informações relevantes.
Este módulo fornece a classe ObjetoTag para extrair e formatar dados de tags <h3> e <a> em documentos HTML.

Classes:
    ObjetoTag: Processa tags HTML e converte os dados extraídos em JSON.

Métodos:
    processar_tags(html: str) -> str: Processa as tags HTML e retorna os dados em formato JSON.
    _extrair_tags(self) -> ResultSet[Tag]: Extrai tags <h3> e <a> do HTML.
    _processar_tag(self, tag: Tag) -> Dict[str, str]: Processa uma tag específica e retorna os dados formatados.
    
"""

import json
from typing import Dict
from bs4 import BeautifulSoup, Tag, ResultSet


class ObjetoTag:
    """
    Classe para processar tags HTML e extrair informações relevantes.

    Args:
        html (str): O HTML a ser processado.

    Métodos:
        processar_tags: Processa tags <h3> e <a> e retorna os dados em JSON.
    """

    def __init__(self, html: str):
        """
        Inicializa a classe com o HTML fornecido.

        Args:
            html (str): O conteúdo HTML a ser processado.
        """
        self.html = html

    def _extrair_tags(self) -> ResultSet[Tag]:
        """
        Extrai tags <h3> e <a> do HTML usando BeautifulSoup.

        Returns:
            ResultSet[Tag]: Lista de tags extraídas.
        """
        soup = BeautifulSoup(self.html, "html.parser")
        return soup.find_all(["h3", "a"])

    def _processar_tag(self, tag: Tag) -> Dict[str, str]:
        """
        Processa uma tag específica e retorna os dados formatados.

        Args:
            tag (Tag): A tag HTML a ser processada.

        Returns:
            Dict[str, str]: Dados formatados da tag.
        """
        return {
            "tag_name": tag.name,
            "text_content": tag.get_text(strip=True) or "",
            "attributes": {k.lower(): v for k, v in tag.attrs.items()},
        }

    def processar_tags(self) -> str:
        """
        Processa tags <h3> e <a> e retorna os dados em formato JSON.

        Returns:
            str: JSON com as informações das tags processadas.
        """
        tags: ResultSet[Tag] = self._extrair_tags()
        resultado: Dict[str, Dict[str, str]] = {
            f"tag_{i + 1}": self._processar_tag(tag) for i, tag in enumerate(tags)
        }
        return json.dumps(resultado, indent=4, ensure_ascii=False)


# # Exemplo de uso com HTML de teste
# if __name__ == "__main__":
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

#     processador = ObjetoTag(html=HTML_TESTE)
#     resultado_processado = processador.processar_tags()
#     print(resultado_processado)
