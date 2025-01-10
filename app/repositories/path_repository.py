# app/repositories/path_repository.py
# pylint: disable=E0401

"""
Repositório genérico para manipulação de itens no sistema de arquivos.
"""

from pathlib import Path
from typing import List, Dict, Union
from models import ItemSistema


class PathRepository:
    """
    Repositório genérico para manipulação de itens no sistema de arquivos.
    """

    @staticmethod
    def buscar_item(caminho: Path) -> ItemSistema:
        """
        Busca um item genérico no sistema de arquivos.

        Args:
            caminho (Path): Caminho do item a ser buscado.

        Returns:
            ItemSistema: Instância representando o item no sistema de arquivos.

        Raises:
            FileNotFoundError: Se o caminho não existir.
        """
        if caminho.exists():
            return ItemSistema(caminho)
        raise FileNotFoundError(f"O caminho {caminho} não existe.")

    @staticmethod
    def listar_itens(diretorio: Path) -> List[ItemSistema]:
        """
        Lista todos os itens (arquivos ou subdiretórios) em um diretório.

        Args:
            diretorio (Path): Caminho do diretório a ser listado.

        Returns:
            List[ItemSistema]: Lista de itens no diretório.

        Raises:
            NotADirectoryError: Se o caminho fornecido não for um diretório.
        """
        if not diretorio.is_dir():
            raise NotADirectoryError(f"{diretorio} não é um diretório válido.")

        return [ItemSistema(item) for item in diretorio.iterdir() if item.exists()]

    @staticmethod
    def ajustar_caminhos(
        lista_caminhos: List[str], max_tentativas: int = 10
    ) -> List[Path]:
        """
        Ajusta caminhos relativos e valida a existência.

        Args:
            lista_caminhos (List[str]): Lista de caminhos a serem ajustados.
            max_tentativas (int): Número máximo de tentativas para ajustar caminhos relativos.

        Returns:
            List[Path]: Lista de caminhos ajustados e validados.
        """
        caminhos_ajustados = []
        for caminho_str in lista_caminhos:
            caminho = Path(caminho_str).resolve()
            if caminho.exists():
                caminhos_ajustados.append(caminho)
            elif caminho_str.startswith("../"):
                tentativas = 0
                while tentativas < max_tentativas:
                    caminho = Path("../") / caminho
                    if caminho.exists():
                        caminhos_ajustados.append(caminho.resolve())
                        break
                    tentativas += 1
        return caminhos_ajustados

    @staticmethod
    def validar_json(json_caminhos: Dict[str, Union[List, dict]]) -> bool:
        """
        Valida a estrutura do JSON de entrada.

        Args:
            json_caminhos (dict): JSON contendo os caminhos para validação.

        Returns:
            bool: True se o JSON for válido, False caso contrário.
        """
        if not (
            "jsonEntrada" in json_caminhos
            and isinstance(json_caminhos["jsonEntrada"], list)
        ):
            return False
        # Valida se todos os itens da lista são strings (opcional)
        return all(isinstance(item, str) for item in json_caminhos["jsonEntrada"])
