# pylint: disable=C, R, E, W

import os
from typing import Dict, Optional


def extrair_pasta_mae(caminho: str) -> Optional[str]:
    """Extrai a pasta mãe do caminho fornecido."""
    diretorios = os.path.normpath(caminho).split(os.sep)
    return diretorios[-2] if len(diretorios) > 1 else None


# Funções para manipulação de permissões e identificadores
def obter_permissoes_caminho(caminho: str) -> Dict[str, bool]:
    """
    Verifica e retorna as permissões de leitura, escrita e execução para o caminho.
    """
    if not os.path.exists(caminho):
        return str(f"O caminho '{caminho}' não existe.")
    return {
        "leitura": os.access(caminho, os.R_OK),
        "escrita": os.access(caminho, os.W_OK),
        "execucao": os.access(caminho, os.X_OK),
    }


def extrair_nome_item(caminho: str) -> Optional[str]:
    """Extrai o nome do item (arquivo ou pasta) do caminho fornecido."""
    if caminho.endswith(os.sep):
        caminho = caminho[:-1]
    return os.path.basename(caminho) if caminho else None
