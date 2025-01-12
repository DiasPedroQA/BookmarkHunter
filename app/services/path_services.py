"""
Este módulo contém funções auxiliares para manipulação de caminhos e datas.

Funções:
    - obter_dados_caminho(caminho_resolvido: str) -> dict[str, str]: 
        Obtém informações detalhadas sobre um caminho fornecido.
    - obter_tamanho_arquivo(tamanho_arquivo: int) -> str: 
        Retorna o tamanho de um arquivo em formato legível (KB, MB, etc.).
    - obter_data_criacao(timestamp_data_criacao: float) -> str: 
        Retorna a data de criação de um arquivo no formato padrão.
    - obter_data_modificacao(timestamp_data_modificacao: float) -> str: 
        Retorna a data de modificação de um arquivo no formato padrão.
    - obter_data_acesso(timestamp_data_acesso: float) -> str: 
        Retorna a data de acesso de um arquivo no formato padrão.
    - obter_permissoes_caminho(caminho: str) -> dict[str, bool]: 
        Retorna as permissões do caminho fornecido (leitura, escrita e execução).
    - obter_id_unico(identificador: int) -> str: 
        Gera um ID único a partir de um identificador numérico positivo.
    - sanitizar_caminho_relativo(caminho: str) -> str: 
        Remove caracteres especiais e normaliza caminhos relativos.
"""

from datetime import datetime
import os
import uuid


def _fatiar_caminho(caminho_inteiro: str, separador: str = "/") -> list[str]:
    """
    Divide um caminho em partes utilizando um separador e remove itens irrelevantes.

    Args:
        caminho_inteiro (str): O caminho completo que será dividido.
        separador (str, opcional): O caractere separador usado para dividir o caminho.
            Padrão é "/".

    Returns:
        list[str]: Lista contendo as partes válidas do caminho, sem itens vazios ou irrelevantes.

    Raises:
        ValueError: Se o caminho não for uma string válida.
    """
    try:
        fatias = caminho_inteiro.strip(separador).split(separador)
        return [fatia for fatia in fatias if fatia not in ("", "..")]
    except AttributeError as exc:
        raise ValueError("O caminho deve ser uma string válida.") from exc


def _formatar_data(timestamp: float) -> str:
    """
    Converte um timestamp em uma data legível no formato "dd/mm/yyyy hh:mm:ss".

    Args:
        timestamp (float): O timestamp que será formatado.

    Returns:
        str: A data formatada no padrão "dd/mm/yyyy hh:mm:ss", ou uma mensagem de erro.
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")
    except (ValueError, TypeError) as exc:
        return f"Erro ao formatar a data: {exc}"


def obter_dados_caminho(caminho_resolvido: str) -> dict[str, str]:
    """
    Extrai informações detalhadas de um caminho, como o diretório pai, nome e extensão.

    Args:
        caminho_resolvido (str): O caminho completo do arquivo ou diretório.

    Returns:
        dict[str, str]: Um dicionário contendo:
            - "pasta_pai": Diretório pai do item.
            - "nome_arquivo": Nome do arquivo (se presente).
            - "extensao_arquivo": Extensão do arquivo (se presente).
            - "nome_pasta": Nome da pasta (se o caminho for um diretório).
    """
    fatias = _fatiar_caminho(caminho_resolvido)
    dados = {"pasta_pai": "/".join(fatias[:-1]) if len(fatias) > 1 else ""}

    if fatias:
        item = fatias[-1]
        if "." in item and not item.endswith("."):
            nome_arquivo, extensao_arquivo = item.rsplit(".", 1)
            dados.update(
                {"nome_arquivo": nome_arquivo, "extensao_arquivo": extensao_arquivo}
            )
        else:
            dados.update({"nome_pasta": item})

    return dados


def obter_data_criacao(timestamp_data_criacao: float) -> str:
    """
    Retorna a data de criação do arquivo no formato "dd/mm/yyyy hh:mm:ss".

    Args:
        timestamp_data_criacao (float): O timestamp da data de criação.

    Returns:
        str: A data de criação formatada.
    """
    return _formatar_data(timestamp_data_criacao)


def obter_data_modificacao(timestamp_data_modificacao: float) -> str:
    """
    Retorna a data de modificação do arquivo no formato "dd/mm/yyyy hh:mm:ss".

    Args:
        timestamp_data_modificacao (float): O timestamp da data de modificação.

    Returns:
        str: A data de modificação formatada.
    """
    return _formatar_data(timestamp_data_modificacao)


def obter_data_acesso(timestamp_data_acesso: float) -> str:
    """
    Retorna a data de acesso do arquivo no formato "dd/mm/yyyy hh:mm:ss".

    Args:
        timestamp_data_acesso (float): O timestamp da data de acesso.

    Returns:
        str: A data de acesso formatada.
    """
    return _formatar_data(timestamp_data_acesso)


def obter_permissoes_caminho(caminho: str) -> dict[str, bool]:
    """
    Verifica e retorna as permissões do caminho fornecido.

    Args:
        caminho (str): O caminho do sistema de arquivos.

    Returns:
        dict[str, bool]: Dicionário com permissões:
            - "leitura": Verdadeiro se o caminho é legível.
            - "escrita": Verdadeiro se o caminho é gravável.
            - "execucao": Verdadeiro se o caminho é executável.

    Raises:
        FileNotFoundError, PermissionError, OSError: Em caso de falhas ao acessar o caminho.
    """
    try:
        return {
            "leitura": os.access(caminho, os.R_OK),
            "escrita": os.access(caminho, os.W_OK),
            "execucao": os.access(caminho, os.X_OK),
        }
    except (FileNotFoundError, PermissionError, OSError) as erro:
        raise erro


def obter_id_unico(identificador: int) -> str:
    """
    Gera um ID único baseado em um identificador numérico positivo.

    Args:
        identificador (int): O identificador numérico.

    Returns:
        str: Um ID único gerado.

    Raises:
        ValueError: Se o identificador for menor ou igual a zero.
    """
    if identificador <= 0:
        raise ValueError("O identificador deve ser um número inteiro positivo.")
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(identificador)))


def sanitizar_caminho_relativo(caminho: str) -> str:
    """
    Remove caracteres especiais de um caminho relativo e o normaliza.

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
