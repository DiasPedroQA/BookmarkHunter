# pylint: disable=C, R, E, W

"""
Módulo auxiliar para manipulação de caminhos e datas.

Funções disponíveis:
1. Manipulação de datas:
    - obter_data_criacao
    - obter_data_modificacao
    - obter_data_acesso
2. Manipulação de permissões e identificadores:
    - obter_permissoes_caminho
    - obter_id_unico
3. Manipulação de caminhos:
    - sanitizar_caminho
    - validar_tamanho_nome_caminho
    - verificar_caminho_absoluto
    - verificar_caminho_relativo
    - contar_diretorios
    - extrair_nome_item
    - extrair_pasta_principal
    - extrair_pasta_mae
    - verificar_arquivo
    - sanitizar_prefixo_caminho
"""

import datetime
import re
from typing import Dict, Optional


def get_regex_pattern(regex_name: str) -> str:
    # Constantes de expressões regulares
    REGEX_UTEIS: Dict[str, str] = {
        "CAMINHO_ABSOLUTO": r"^(?:[a-zA-Z]:\\|/home/[a-zA-Z0-9_-]+/)",  # Windows e Linux
        "CAMINHO_RELATIVO": r"^(?:\.{1,2}/)",  # Caminho relativo
        "NOME_ITEM": r"\.[a-zA-Z0-9]+$",  # Extensão de arquivos
        "SANITIZAR_CAMINHO": r"[^a-zA-Z0-9\- _./\\:]",  # Caracteres inválidos
        "EXTRAIR_PASTA": r"([^/\\]+)/[^/\\]+/?$",  # Pasta principal
        "VALIDACAO_CAMINHO": r"[\\/]+",  # Validar e normalizar barras
    }
    if regex_name not in REGEX_UTEIS:
        raise KeyError(f"Expressão regular '{regex_name}' não encontrada.")
    return REGEX_UTEIS[regex_name]



def validar_caminho(caminho: str, separador: str = "/") -> str:
    """
    Valida e normaliza um caminho fornecido.
    """
    if not isinstance(caminho, str) or not caminho.strip():
        raise ValueError("O caminho deve ser uma string não vazia.")

    regex_validacao = get_regex_pattern("VALIDACAO_CAMINHO")
    # if not regex_validacao:
    #     raise KeyError("Expressão regular para validação de caminho não encontrada.")

    # Remove múltiplos separadores consecutivos e espaços nas extremidades
    caminho_normalizado = re.sub(regex_validacao, separador, caminho.strip())
    return caminho_normalizado.rstrip(separador)


def sanitizar_caminho(caminho: str) -> str:
    """
    Remove caracteres inválidos do caminho e normaliza-o.
    """
    caminho_normalizado = validar_caminho(caminho)
    if regex_sanitizacao := get_regex_pattern("SANITIZAR_CAMINHO"):
        return re.sub(regex_sanitizacao, "", caminho_normalizado)
    # else:
    #     raise KeyError("Expressão regular para sanitização de caminho não encontrada.")


def verificar_caminho_absoluto(caminho: str) -> bool:
    """
    Verifica se o caminho fornecido é absoluto.
    """
    caminho_normalizado = validar_caminho(caminho)
    if regex_absoluto := get_regex_pattern("CAMINHO_ABSOLUTO"):
        return bool(re.match(regex_absoluto, caminho_normalizado))
    # else:
    #     raise KeyError(
    #         "Expressão regular para verificar caminho absoluto não encontrada."
    #     )


def verificar_caminho_relativo(caminho: str) -> bool:
    """
    Verifica se o caminho fornecido é relativo.
    """
    caminho_normalizado = validar_caminho(caminho)
    if regex_relativo := get_regex_pattern("CAMINHO_RELATIVO"):
        return bool(re.match(regex_relativo, caminho_normalizado))
    # else:
    #     raise KeyError(
    #         "Expressão regular para verificar caminho relativo não encontrada."
    #     )


def extrair_pasta_principal(caminho: str) -> Optional[str]:
    """
    Extrai a pasta principal do caminho fornecido.
    """
    caminho_normalizado = validar_caminho(caminho)
    regex_pasta = get_regex_pattern("EXTRAIR_PASTA")
    # if not regex_pasta:
    #     raise KeyError("Expressão regular para extrair pasta não encontrada.")

    match = re.search(regex_pasta, caminho_normalizado)
    return match[1] if match else None


def verificar_arquivo(caminho: str) -> bool:
    """
    Verifica se o caminho representa um arquivo.
    """
    caminho_normalizado = validar_caminho(caminho)
    if regex_arquivo := get_regex_pattern("NOME_ITEM"):
        return bool(re.search(regex_arquivo, caminho_normalizado))
    # else:
    #     raise KeyError("Expressão regular para verificar arquivos não encontrada.")


# Funções para manipulação de datas
def _formatar_data(timestamp: float) -> str:
    """
    Converte um timestamp em uma data legível no formato 'dd/mm/yyyy hh:mm:ss'.
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
    except (OSError, ValueError) as erro:
        return f"Erro ao formatar data: {erro}"


def obter_data_criacao(timestamp: float) -> str:
    """Retorna a data de criação formatada a partir de um timestamp."""
    return _formatar_data(timestamp)


def obter_data_modificacao(timestamp: float) -> str:
    """Retorna a data de modificação formatada a partir de um timestamp."""
    return _formatar_data(timestamp)


def obter_data_acesso(timestamp: float) -> str:
    """Retorna a data de acesso formatada a partir de um timestamp."""
    return _formatar_data(timestamp)


# # Funções para manipulação de identificadores
# def obter_id_unico(identificador: int) -> str:
#     """Gera um UUID baseado em um identificador numérico positivo."""
#     if identificador <= 0:
#         raise ValueError("O identificador deve ser um número inteiro positivo.")
#     return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(identificador)))


# # Funções para manipulação de permissões e identificadores
# def obter_permissoes_caminho(caminho: str) -> Dict[str, bool]:
#     """
#     Verifica e retorna as permissões de leitura, escrita e execução para o caminho.
#     """
#     if not os.path.exists(caminho):
#         raise FileNotFoundError(f"O caminho '{caminho}' não existe.")
#     return {
#         "leitura": os.access(caminho, os.R_OK),
#         "escrita": os.access(caminho, os.W_OK),
#         "execucao": os.access(caminho, os.X_OK),
#     }


# def validar_tamanho_nome_caminho(caminho: str) -> bool:
#     """Valida se o tamanho do caminho não excede o limite de 260 caracteres."""
#     if len(caminho) > 260:
#         raise ValueError(f"O caminho '{caminho}' excede o limite de 260 caracteres.")
#     return True


# def contar_diretorios(caminho: str) -> int:
#     """Conta o número de diretórios no caminho fornecido."""
#     separador: str = "/"
#     return caminho.count(separador) - 1


# def extrair_nome_item(caminho: str) -> Optional[str]:
#     """Extrai o nome do item (arquivo ou pasta) do caminho fornecido."""
#     return os.path.basename(caminho) if caminho else None


# def extrair_pasta_mae(caminho: str) -> Optional[str]:
#     """Extrai a pasta mãe do caminho fornecido."""
#     diretorios = os.path.normpath(caminho).split(os.sep)
#     return diretorios[-2] if len(diretorios) > 1 else None


# def sanitizar_prefixo_caminho(caminho: str) -> str:
#     """Remove prefixos inválidos e normaliza caminhos relativos."""
#     caminho = caminho.lstrip("/\\.")
#     return caminho


# # Teste das funções
# def main():
#     # Valores para testar as funções de data
#     valores_teste_data = [1737658061.00, "string inválida", -12345, None]

#     print("\n=== Testando Funções de Data ===")
#     for valor in valores_teste_data:
#         print(f"\nTestando com valor: {valor}")
#         try:
#             print(f"Data de acesso: {obter_data_acesso(valor)}")
#             print(f"Data de criação: {obter_data_criacao(valor)}")
#             print(f"Data de modificação: {obter_data_modificacao(valor)}")
#         except Exception as erro:
#             print(f"Erro encontrado: {erro}")

#     # Valores para testar a função de ID único
#     valores_teste_id = [42, -1, "string", 0, None, 999, 123456]

#     print("\n=== Testando Função de ID Único ===")
#     for valor in valores_teste_id:
#         print(f"\nTestando com identificador: {valor}")
#         try:
#             print(f"ID único gerado: {obter_id_unico(valor)}")
#         except Exception as erro:
#             print(f"Erro encontrado: {erro}")


# def secondary():
#     """Testa as funções de manipulação de caminhos com diferentes tipos de entradas."""
#     tipos_de_caminhos: Dict[str, str] = {
#         "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "Arquivo - Relativo e válido": "../imagens/foto.jpg",
#         "Arquivo - Absoluto e inválido": "/home/pedro-pm-dias/arquivo?*<>.html",
#         "Arquivo - Relativo e inválido": "../imagens/arquivo?*<>.jpg",
#         "Pasta - Absoluta e válida": "/home/pedro-pm-dias/Downloads/Chrome/",
#         "Pasta - Relativa e válida": "./Downloads/Chrome/",
#         "Pasta - Absoluta e inválida": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
#         "Pasta - Relativa e inválida": "./Downloads/Chrome/<>/",
#     }

#     print("\n=== Testando Funções de Manipulação de Caminhos ===")

#     for tipo, caminho_teste in tipos_de_caminhos.items():
#         print(f"\nTipo do caminho: {tipo}")
#         print(f"Caminho original: {caminho_teste}")

#         try:
#             # Sanitização do caminho
#             caminho_sanitizado = sanitizar_caminho(caminho_teste)
#             print(f"Caminho sanitizado: {caminho_sanitizado}")

#             # Validação do tamanho do caminho
#             if validar_tamanho_nome_caminho(caminho_sanitizado):
#                 print("Validação de tamanho: OK")

#             # Verificação de caminho absoluto ou relativo
#             if verificar_caminho_absoluto(caminho_sanitizado):
#                 print("O caminho é absoluto.")
#             elif verificar_caminho_relativo(caminho_sanitizado):
#                 print("O caminho é relativo.")
#             else:
#                 print("O caminho não é reconhecido como absoluto ou relativo.")

#             # Contar diretórios
#             num_diretorios = contar_diretorios(caminho_sanitizado)
#             print(f"Número de diretórios: {num_diretorios}")

#             # Extração de informações do caminho
#             nome_item = extrair_nome_item(caminho_sanitizado)
#             print(f"Nome do item: {nome_item}")

#             pasta_principal = extrair_pasta_principal(caminho_sanitizado)
#             print(f"Pasta principal: {pasta_principal}")

#             pasta_mae = extrair_pasta_mae(caminho_sanitizado)
#             print(f"Pasta mãe: {pasta_mae}")

#             # Verificar se é um arquivo
#             if verificar_arquivo(caminho_sanitizado):
#                 print("O caminho representa um arquivo.")
#             else:
#                 print("O caminho não representa um arquivo.")

#             # Verificar permissões do caminho
#             permissoes = obter_permissoes_caminho(caminho_sanitizado)
#             print(f"Permissões do caminho: {permissoes}")

#             # Sanitizar prefixo do caminho
#             caminho_prefixo_sanitizado = sanitizar_prefixo_caminho(caminho_sanitizado)
#             print(f"Caminho com prefixo sanitizado: {caminho_prefixo_sanitizado}")

#         except Exception as erro:
#             print(f"Erro ao processar o caminho '{caminho_teste}': {erro}")


# if __name__ == "__main__":
#     main()
#     secondary()
