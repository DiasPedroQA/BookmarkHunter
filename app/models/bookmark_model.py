# app/models/bookmark_model.py

"""
Classe para processar tags HTML e extrair informações relevantes.
"""

from typing import Dict
import json
import time
from datetime import datetime
import hashlib
import uuid
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

    def _converter_timestamp(self, timestamp: str) -> str:
        """
        Converte o timestamp para o formato de data e hora (BR: dd/mm/yyyy hh:mm:ss).
        """
        try:
            timestamp_int = int(timestamp)
            data = datetime.fromtimestamp(timestamp_int)
            return data.strftime("%d/%m/%Y %H:%M:%S")
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
        tag_data = {
            "id": self._gerar_id(),
            "text_content": tag.text.strip(),
            "add_date": self._converter_timestamp(
                tag.attrs.get("ADD_DATE", "Não encontrado")
            ),
            "tag_name": tag.name,
        }

        if tag.name == "h3":
            tag_data["last_modified"] = self._converter_timestamp(
                tag.attrs.get("LAST_MODIFIED", "Não encontrado")
            )
        elif tag.name == "a":
            tag_data["href"] = tag.attrs.get("href", "Não encontrado")

        return tag_data

    def processar_tags(self) -> str:
        """
        Processa todas as tags extraídas e retorna um JSON com as informações.
        """
        resultado = {}
        for idx, tag in enumerate(self.tags):
            tag_id = f"tag_{idx + 1}"  # Geração de id com prefixo "tag_"
            resultado[tag_id] = self._processar_tag(tag)

        return json.dumps(resultado, indent=4)

    @staticmethod
    def converter_timestamp_para_data(timestamp: str) -> str:
        """
        Converte um timestamp Unix para o formato DD/MM/YYYY HH:mm:ss.
        Retorna 'Formato inválido' se o timestamp não for válido.
        """
        try:
            # Converte para inteiro e depois para data
            timestamp_int = int(timestamp)
            data_formatada = datetime.fromtimestamp(timestamp_int).strftime(
                "%d/%m/%Y %H:%M:%S"
            )
            return data_formatada
        except (ValueError, TypeError):
            return "Formato inválido"

    def extrair_dados_tag(self, tag):
        """
        Extrai os dados da tag e retorna um dicionário com os dados.
        """
        add_date = tag.attrs.get("add_date", None)
        last_modified = tag.attrs.get("last_modified", None)

        data = {
            "id": str(uuid.uuid4()),
            "tag_name": tag.name,
            "text_content": tag.text.strip() if tag.text else "",
            "add_date": (
                self.converter_timestamp_para_data(add_date) if add_date else None
            ),
            "last_modified": (
                self.converter_timestamp_para_data(last_modified)
                if last_modified
                else None
            ),
        }

        if tag.name == "a":
            data["href"] = tag.attrs.get("href", None)

        return {k: v for k, v in data.items() if v is not None}
