# app/models/bookmark_model.py

"""
Classe para processar tags HTML e extrair informações relevantes.
"""

from typing import Dict
import json
import time
from datetime import datetime, timezone
import hashlib
from bs4 import BeautifulSoup


class TagProcessor:
    """
    Classe para processar tags HTML e extrair informações relevantes.

    Args:
        html (str): O HTML a ser processado.

    Returns:
        str: JSON contendo as informações extraídas.

    Exemplo de uso:
    ```
    html = "<html><body><h3>Título da lista</h3><a href='https://example.com'>Link do item</a></body></html>"
    processor = TagProcessor(html)
    resultado = processor.processar_tags()
    print(resultado)
    ```
    """

    def __init__(self, html: str):
        self.html = html
        self.tags = self._extrair_tags()

    def _extrair_tags(self) -> list:
        """
        Extrai somente as tags <a> e <h3> do HTML.
        """
        soup = BeautifulSoup(self.html, "html.parser")
        return soup.find_all(["h3", "a"])  # Extrai somente as tags <h3> e <a>

    @staticmethod
    def _formatar_timestamp(timestamp: str) -> str:
        """
        Converte um timestamp Unix para o formato DD/MM/YYYY HH:mm:ss.
        Retorna 'Formato inválido' se o timestamp não for válido.
        """
        try:
            timestamp_int = int(timestamp)
            data_formatada = datetime.fromtimestamp(
                timestamp_int,
                tz=timezone.utc
            ).strftime(
                "%d/%m/%Y %H:%M:%S"
            )
            return data_formatada
        except (ValueError, TypeError):
            return "Formato inválido"

    def _gerar_id(self) -> str:
        """
        Gera um ID único para cada tag.
        """
        return hashlib.md5(str(time.time()).encode()).hexdigest()

    def _processar_tag(self, tag) -> Dict:
        """
        Processa uma tag específica e retorna os dados formatados.
        """
        tag_attrs = {k.lower(): v for k, v in tag.attrs.items()}  # Normaliza os atributos para minúsculas
        tag_data = {
            "id": self._gerar_id(),
            "text_content": tag.text.strip(),
            "add_date": self._formatar_timestamp(tag_attrs.get("add_date", "")),
            "tag_name": tag.name,
        }

        if tag.name == "h3":
            tag_data["last_modified"] = self._formatar_timestamp(
                tag_attrs.get("last_modified", "")
            )
        elif tag.name == "a":
            tag_data["href"] = tag_attrs.get("href", "Não encontrado")

        return {k: v for k, v in tag_data.items() if v != "Não encontrado" and v is not None}

    def processar_tags(self) -> str:
        """
        Processa todas as tags extraídas e retorna um JSON com as informações.
        """
        resultado = {}
        for idx, tag in enumerate(self.tags):
            tag_id = f"tag_{idx + 1}"  # Geração de id com prefixo "tag_"
            resultado[tag_id] = self._processar_tag(tag)

        return json.dumps(resultado, indent=4, ensure_ascii=False)


# Exemplo de uso
# if __name__ == "__main__":
#     HTML_TESTE = """
#     <html>
#         <body>
#             <h3 add_date="1699349340">Título da lista</h3>
#             <a href="https://example.com">Link do item</a>
#             <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#         <DL><p>
#             <DT><A HREF="https://dev.to/leandronsp/pt-br-fundamentos-do-git-um-guia-completo-2djh" ADD_DATE="1686055702" ICON="data:image/png;base64,...">[pt-BR] Fundamentos do Git, um guia completo - DEV Community</A>
#             <DT><H3 ADD_DATE="1686621554" LAST_MODIFIED="1721823235">Estudos</H3>
#         <DL><p>
#             <DT><A HREF="https://martinfowler.com/articles/practical-test-pyramid.html" ADD_DATE="1691737793" ICON="data:image/png;base64,...">A Pirâmide do Teste Prático</A>
#         </body>
#     </html>
#     """

#     # Criar uma instância da classe TagProcessor
#     processador = TagProcessor(html=HTML_TESTE)
#     html_teste_processado = processador.processar_tags()
#     print(html_teste_processado)
