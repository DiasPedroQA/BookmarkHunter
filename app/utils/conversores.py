# app/utils/conversores.py

"""
Módulo de utilitários para conversão e manipulação de dados.
"""

from datetime import datetime
import re
import json


class ConversoresUtils:
    """
    Classe de utilitários para conversão e manipulação de dados.
    """

    @staticmethod
    def converter_timestamp_para_data_hora_br(tag_timestamp: str) -> str:
        """
        Converte um timestamp para o formato de data e hora brasileiro (dd/mm/yyyy HH:mm:ss).
        """
        try:
            timestamp = int(tag_timestamp)
            data_hora = datetime.fromtimestamp(timestamp)
            return data_hora.strftime("%d/%m/%Y %H:%M:%S")
        except (ValueError, TypeError):
            return ""  # Retorna uma string vazia se o timestamp for inválido

    @staticmethod
    def converter_tamanho_arquivo(tamanho_bytes: int) -> str:
        """
        Converte o tamanho de um arquivo em bytes para uma string formatada.

        Args:
            tamanho_bytes (int): Tamanho do arquivo em bytes.

        Returns:
            str: Tamanho do arquivo formatado (B, KB, MB, GB, ou TB).
        """
        if tamanho_bytes < 0:
            return "Tamanho inválido"

        unidades = ["B", "KB", "MB", "GB", "TB"]
        tamanho = float(tamanho_bytes)
        for unidade in unidades:
            if tamanho < 1024:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024
        return f"{tamanho:.2f} PB"  # Caso o tamanho exceda TB, retorna em PB

    @staticmethod
    def limpar_texto(texto: str) -> str:
        """
        Limpa o texto removendo espaços extras no início/fim e caracteres especiais.
        """
        return " ".join(texto.split())

    @staticmethod
    def texto_para_url_amigavel(texto: str) -> str:
        """
        Converte um texto para uma URL amigável (sem espaços, acentos, etc).
        """
        texto = texto.lower()
        texto = re.sub(r"[^a-z0-9]", "-", texto)
        texto = re.sub(r"-+", "-", texto)
        texto = texto.strip("-")
        return texto

    @staticmethod
    def json_para_dict(json_string: str) -> dict:
        """
        Converte uma string JSON para um dicionário Python.
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return {}  # Retorna um dicionário vazio se o JSON for inválido

    @staticmethod
    def dict_para_json(dicionario: dict) -> str:
        """
        Converte um dicionário Python para uma string JSON.
        """
        return json.dumps(dicionario, indent=4, ensure_ascii=False)
