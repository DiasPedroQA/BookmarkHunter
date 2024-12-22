# app/utils/conversores.py

"""
Arquivo de utilidades para conversão de dados úteis para o projeto.
"""

from datetime import datetime, timezone


def formatar_timestamp(timestamp: str) -> str:
    """
    Converte um timestamp Unix para o formato DD/MM/YYYY HH:mm:ss.
    Retorna 'Formato inválido' se o timestamp não for válido.
    """
    try:
        timestamp_int: int = int(timestamp)
        data_formatada: datetime = datetime.fromtimestamp(
            timestamp_int, tz=timezone.utc
        ).strftime("%d/%m/%Y %H:%M:%S")
        return data_formatada
    except (ValueError, TypeError):
        return "Formato inválido"
