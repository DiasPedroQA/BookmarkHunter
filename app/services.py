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
import os
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

    Levanta:
        ValueError: Se o caminho não for uma string válida.
    """
    try:
        fatias = caminho_inteiro.strip(separador).split(separador)
        return [fatia for fatia in fatias if fatia not in ("", "..")]
    except AttributeError as exc:
        raise ValueError("O caminho deve ser uma string válida.") from exc


def _formatar_data(timestamp: float) -> str:
    """
    Formata um timestamp para o formato "dd/mm/yyyy hh:mm:ss".

    Parâmetros:
        timestamp (float): O timestamp a ser formatado.

    Retorna:
        str: O timestamp formatado.
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
    except ValueError as exc:
        return "Data inválida. Verifique o timestamp -> " + str(exc)
    except TypeError as exc:
        return "Tipo de dado inválido. Verifique o timestamp -> " + str(exc)


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
    Calcula o tamanho de um arquivo em unidades legíveis (KB, MB, GB, etc.).
    
    Args:
        numero (int): O tamanho do arquivo em bytes.

    Returns:
        str: Uma string indicando o valor convertido e a unidade correspondente.
    """
    if tamanho_arquivo <= 0:
        raise ValueError("O tamanho deve ser maior que zero.")

    unidades = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    contador = 0

    while tamanho_arquivo >= 1024 and contador < len(unidades) - 1:
        tamanho_arquivo /= 1024
        contador += 1

    return f"{tamanho_arquivo:.2f} {unidades[contador]}"


def obter_data_criacao(timestamp_data_criacao: float) -> str:
    """
    Obtém a data de criação do arquivo a partir de um timestamp.

    Parâmetros:
        timestamp_data_criacao (float): O timestamp da data de criação do arquivo.

    Retorna:
        str: A data de criação do arquivo no formato "dd/mm/yyyy hh:mm:ss".
    """
    return _formatar_data(timestamp_data_criacao)


def obter_data_modificacao(timestamp_data_modificacao: float) -> str:
    """
    Obtém a data de modificação do arquivo a partir de um timestamp.

    Parâmetros:
        timestamp_data_modificacao (float): O timestamp da data de modificação do arquivo.

    Retorna:
        str: A data de modificação do arquivo no formato "dd/mm/yyyy hh:mm:ss".
    """
    return _formatar_data(timestamp_data_modificacao)


def obter_data_acesso(timestamp_data_acesso: float) -> str:
    """
    Obtém a data de acesso do arquivo a partir de um timestamp.

    Parâmetros:
        timestamp_data_acesso (float): O timestamp da data de acesso do arquivo.

    Retorna:
        str: A data de acesso do arquivo no formato "dd/mm/yyyy hh:mm:ss".
    """
    return _formatar_data(timestamp_data_acesso)


def obter_permissoes_caminho(caminho: str) -> dict[str, bool]:
    """
    Obtém as permissões do caminho fornecido.

    Args:
        caminho (str): O caminho do sistema de arquivos.

    Returns:
        dict[str, bool]: Um dicionário com as permissões:
            - leitura: Se o caminho pode ser lido.
            - escrita: Se o caminho pode ser escrito.
            - execução: Se o caminho pode ser executado.
    """
    try:
        return {
            "leitura": os.access(caminho, os.R_OK),
            "escrita": os.access(caminho, os.W_OK),
            "execucao": os.access(caminho, os.X_OK),
        }
    except OSError as erro:
        raise OSError(f"Erro ao verificar permissões no caminho '{caminho}': {erro}") from erro


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


def sanitizar_caminho_relativo(caminho: str) -> str:
    """
    Remove caracteres especiais (../) e normaliza o caminho relativo.
    
    Args:
        caminho (str): O caminho relativo a ser sanitizado.

    Returns:
        str: O caminho relativo sanitizado.
    """
    if str(caminho).startswith("/../"):
        caminho = caminho.replace("/../", "../")

    while str(caminho).startswith("../"):
        caminho = caminho[3:]

    return caminho
