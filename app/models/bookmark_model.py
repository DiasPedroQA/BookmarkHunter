# app/models/bookmark_model.py
# pylint: disable = C

from typing import Dict
import json
import time
from datetime import datetime
import hashlib
from bs4 import BeautifulSoup


class TagProcessor:
    def __init__(self, html: str):
        self.html = html
        self.tags = self._extrair_tags()

    def _extrair_tags(self) -> list:
        """
        Extrai somente as tags <a> e <h3> do HTML.
        """
        soup = BeautifulSoup(self.html, 'html.parser')
        return soup.find_all(['h3', 'a'])  # Extrai somente as tags <h3> e <a>

    def _converter_timestamp(self, timestamp: str) -> str:
        """
        Converte o timestamp para o formato de data e hora (BR: dd/mm/yyyy hh:mm:ss).
        """
        try:
            timestamp_int = int(timestamp)
            data = datetime.fromtimestamp(timestamp_int)
            return data.strftime('%d/%m/%Y %H:%M:%S')
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
            "add_date": self._converter_timestamp(tag.attrs.get("ADD_DATE", "Não encontrado")),
            "tag_name": tag.name
        }

        if tag.name == "h3":
            tag_data["last_modified"] = self._converter_timestamp(tag.attrs.get("LAST_MODIFIED", "Não encontrado"))
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
