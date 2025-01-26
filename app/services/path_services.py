# app/services/path_services.py

# pylint: disable=C, R, E, W

import os
from pathlib import Path
from typing import Dict, Optional


def extrair_pasta_mae(caminho: str) -> Optional[str]:
    """Extrai a pasta mãe do caminho fornecido."""
    caminho_path = Path(caminho).resolve()
    return (
        caminho_path.parent.name if caminho_path.parent != caminho_path.anchor else None
    )


def obter_permissoes_caminho(caminho: str) -> Dict[str, bool]:
    """
    Verifica e retorna as permissões de leitura, escrita e execução para o caminho.
    """
    caminho_path = Path(caminho).resolve()
    if not caminho_path.exists():
        return str(f"O caminho '{caminho}' não existe.")
    return {
        "leitura": caminho_path.is_file() or caminho_path.is_dir(),
        "escrita": os.access(caminho_path, os.W_OK),
        "execucao": os.access(caminho_path, os.X_OK),
    }


def extrair_nome_item(caminho: str) -> Optional[str]:
    """Extrai o nome do item (arquivo ou pasta) do caminho fornecido."""
    caminho_path = Path(caminho).resolve()
    return caminho_path.name if caminho_path.name else None


# def processar_caminhos(caminhos: Dict[str, str]) -> None:
#     """
#     Processa diferentes tipos de caminhos, extraindo informações e verificando permissões.

#     :param caminhos: Um dicionário com tipos de caminhos e seus respectivos valores.
#     """
#     for descricao, caminho in caminhos.items():
#         print(f"\n[Descrição do Caminho]: {descricao}")
#         print(f"[Caminho]: {caminho}")

#         # 1. Extrair a pasta mãe
#         pasta_mae = extrair_pasta_mae(caminho)
#         print(f"  - Pasta Mãe: {pasta_mae if pasta_mae else 'Não disponível'}")

#         # 2. Obter permissões do caminho
#         permissoes = obter_permissoes_caminho(caminho)
#         if isinstance(permissoes, str):
#             print(f"  - Permissões: {permissoes}")  # Erro ou caminho inexistente
#         else:
#             print("  - Permissões:")
#             for tipo, valor in permissoes.items():
#                 print(f"    * {tipo.capitalize()}: {'Sim' if valor else 'Não'}")

#         # 3. Extrair o nome do item
#         nome_item = extrair_nome_item(caminho)
#         print(f"  - Nome do Item: {nome_item if nome_item else 'Não disponível'}")


# # Dicionário de tipos de caminhos para teste
# tipos_de_caminhos: Dict[str, str] = {
#     "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#     "Arquivo - Relativo e válido": "../imagens/foto.jpg",
#     "Arquivo - Absoluto e inválido": "/home/pedro-pm-dias/arquivo?*<>.html",
#     "Arquivo - Relativo e inválido": "../imagens/arquivo?*<>.jpg",
#     "Pasta - Absoluta e válida": "/home/pedro-pm-dias/Downloads/Chrome/",
#     "Pasta - Relativa e válida": "./Downloads/Chrome/",
#     "Pasta - Absoluta e inválida": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
#     "Pasta - Relativa e inválida": "./Downloads/Chrome/<>/",
# }

# # Executar o processamento
# processar_caminhos(tipos_de_caminhos)
