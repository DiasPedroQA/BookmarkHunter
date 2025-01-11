"""
Este módulo contém funções auxiliares para manipulação de caminhos e datas.

Funções:
    - obter_dados_caminho(caminho_resolvido: str) -> dict[str, str]: Obtém informações detalhadas de um caminho.
    - obter_tamanho_arquivo(tamanho_arquivo: int) -> str: Retorna o tamanho do arquivo em formato legível.
    - obter_data_criacao(timestamp_data_criacao: float) -> str: Obtém a data de criação do arquivo.
    - obter_data_modificacao(timestamp_data_modificacao: float) -> str: Obtém a data de modificação do arquivo.
    - obter_data_acesso(timestamp_data_acesso: float) -> str: Obtém a data de acesso do arquivo.
    - obter_permissoes_caminho(permissoes: int) -> str: Retorna as permissões do caminho em formato legível.
    - obter_id_unico(identificador: int) -> str: Gera um ID único a partir de um identificador numérico.
"""

from datetime import datetime
import stat
import uuid


def _fatiar_caminho(caminho_inteiro: str, separador: str = "/") -> list[str]:
    """
    Divide um caminho em partes com base no separador informado, removendo
    partes vazias ou irrelevantes como '..' e '/' no início ou fim.

    Parâmetros:
        caminho_inteiro (str): O caminho completo que será dividido.
        separador (str, opcional): O separador a ser usado para dividir o caminho (padrão é "/").

    Retorna:
        list[str]: Uma lista contendo as partes do caminho, sem os itens vazios ou irrelevantes.
    """
    fatias = caminho_inteiro.strip(separador).split(separador)
    return [fatia for fatia in fatias if fatia not in ("", "..")]


def obter_dados_caminho(caminho_resolvido: str) -> dict[str, str]:
    """
    Obtém informações detalhadas sobre o caminho, como diretório pai, nome do arquivo,
    extensão, ou nome do último item no caminho.

    Parâmetros:
        caminho_resolvido (str): O caminho completo do arquivo ou diretório.

    Retorna:
        dict[str, str]: Um dicionário com as informações do caminho, incluindo:
            - "pasta_pai": O diretório pai do item.
            - "nome_arquivo": O nome do arquivo (se presente).
            - "extensao_arquivo": A extensão do arquivo (se presente).
            - "nome_pasta": O nome da pasta (se o caminho for um diretório).
    """
    fatias = _fatiar_caminho(caminho_resolvido)
    dados = {"pasta_pai": "/".join(fatias[:-1]) if len(fatias) > 1 else ""}

    if fatias:
        item = fatias[-1]
        if "." in item and not item.endswith("."):
            nome, extensao = item.rsplit(".", 1)
            dados.update({"nome_arquivo": nome, "extensao_arquivo": extensao})
        else:
            dados.update({"nome_pasta": item})

    return dados


def obter_tamanho_arquivo(tamanho_arquivo: int) -> str:
    """
    Obtém o tamanho do arquivo em um formato legível, como bytes, KB, MB ou GB.

    Parâmetros:
        tamanho_arquivo (int): O tamanho do arquivo em bytes.

    Retorna:
        str: O tamanho do arquivo formatado de forma legível.
    """
    if tamanho_arquivo < 1024:
        return f"{tamanho_arquivo} bytes"
    if tamanho_arquivo < (1024**2):
        return f"{tamanho_arquivo / 1024:.2f} KB"
    if tamanho_arquivo < (1024**3):
        return f"{tamanho_arquivo / (1024 ** 2):.2f} MB"
    return f"{tamanho_arquivo / (1024 ** 3):.2f} GB"


def obter_data_criacao(timestamp_data_criacao: float) -> str:
    """
    Obtém a data de criação do arquivo a partir de um timestamp.

    Parâmetros:
        timestamp_data_criacao (float): O timestamp da data de criação do arquivo.

    Retorna:
        str: A data de criação do arquivo no formato "dd/mm/yyyy hh:mm:ss".
    """
    return datetime.fromtimestamp(timestamp_data_criacao).strftime("%d/%m/%Y %H:%M:%S")


def obter_data_modificacao(timestamp_data_modificacao: float) -> str:
    """
    Obtém a data de modificação do arquivo a partir de um timestamp.

    Parâmetros:
        timestamp_data_modificacao (float): O timestamp da data de modificação do arquivo.

    Retorna:
        str: A data de modificação do arquivo no formato "dd/mm/yyyy hh:mm:ss".
    """
    return datetime.fromtimestamp(timestamp_data_modificacao).strftime(
        "%d/%m/%Y %H:%M:%S"
    )


def obter_data_acesso(timestamp_data_acesso: float) -> str:
    """
    Obtém a data de acesso do arquivo a partir de um timestamp.

    Parâmetros:
        timestamp_data_acesso (float): O timestamp da data de acesso do arquivo.

    Retorna:
        str: A data de acesso do arquivo no formato "dd/mm/yyyy hh:mm:ss".
    """
    return datetime.fromtimestamp(timestamp_data_acesso).strftime("%d/%m/%Y %H:%M:%S")


def obter_permissoes_caminho(permissoes: int) -> str:
    """
    Obtém as permissões do caminho em formato legível.

    Parâmetros:
        permissoes (int): O valor numérico das permissões do caminho.

    Retorna:
        str: As permissões do caminho no formato legível, como "rwxr-xr-x".
    """
    permissao_legivel = stat.filemode(permissoes)
    return permissao_legivel


def obter_id_unico(identificador: int) -> str:
    """
    Gera um ID único a partir de um identificador numérico positivo.

    Parâmetros:
        identificador (int): O identificador numérico, deve ser maior que zero.

    Retorna:
        str: O ID único gerado.

    Levanta:
        ValueError: Se o identificador não for um número inteiro positivo.
    """
    if identificador <= 0:
        raise ValueError("O identificador deve ser um número inteiro positivo.")
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(identificador)))


# # Exemplo de uso  # pylint: disable=C0103
# if __name__ == "__main__":
#     caminhos = [
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/",
#         "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#         "/caminho/inexistente/",
#         "../../Downloads/Chrome/favoritos_23_12_2024.html",
#         "../../Downloads/Chrome/favoritos.html",
#         "../../Downloads/Chrome/",
#         "../../Downloads/Chrome/Teste/",
#     ]

#     for caminho in caminhos:
#         print(f"\nTeste: {caminho}")
#         caminho_sanitizado = "/".join(_fatiar_caminho(caminho))
#         print(f"Caminho sanitizado: {caminho_sanitizado}")
#         print(f"Dados do caminho: {obter_dados_caminho(caminho_sanitizado)}")
