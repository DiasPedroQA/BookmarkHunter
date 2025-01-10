# app/repositories/folder_repository.py
# pylint: disable=C, E0401

"""
Repositório específico para manipulação de diretórios.
"""

from pathlib import Path
from typing import List
from models import Diretorio
from repositories.path_repository import PathRepository


class FolderRepository(PathRepository):
    """
    Repositório especializado para manipulação de diretórios,
    estendendo funcionalidades do PathRepository.
    """

    @staticmethod
    def buscar_diretorio(caminho: Path) -> Diretorio:
        """
        Busca um diretório no sistema de arquivos.

        Args:
            caminho (Path): Caminho do diretório a ser buscado.

        Returns:
            Diretorio: Objeto representando o diretório.

        Raises:
            NotADirectoryError: Se o caminho não for um diretório válido.
        """
        caminho = PathRepository.validar_diretorio(caminho)  # Valida e ajusta o caminho
        return Diretorio(caminho)

    @staticmethod
    def listar_subdiretorios(diretorio: Path) -> List[Diretorio]:
        """
        Lista todos os subdiretórios dentro de um diretório.

        Args:
            diretorio (Path): Caminho do diretório.

        Returns:
            List[Diretorio]: Lista de objetos Diretorio representando os subdiretórios.

        Raises:
            NotADirectoryError: Se o caminho não for um diretório válido.
        """
        diretorio_obj = FolderRepository.buscar_diretorio(diretorio)
        return [Diretorio(subdir) for subdir in diretorio_obj.caminho.iterdir() if subdir.is_dir()]

    @staticmethod
    def criar_diretorio(caminho: Path, existir_ok: bool = True) -> Diretorio:
        """
        Cria um novo diretório.

        Args:
            caminho (Path): Caminho do diretório a ser criado.
            existir_ok (bool): Se True, não lança erro se o diretório já existir.

        Returns:
            Diretorio: Objeto representando o diretório criado.

        Raises:
            FileExistsError: Se o diretório já existir e `existir_ok` for False.
        """
        if caminho.exists() and not caminho.is_dir():
            raise FileExistsError(f"{caminho} já existe e não é um diretório.")
        caminho.mkdir(parents=True, exist_ok=existir_ok)
        return Diretorio(caminho)

    @staticmethod
    def excluir_diretorio(caminho: Path, forcar: bool = False) -> None:
        """
        Exclui um diretório.

        Args:
            caminho (Path): Caminho do diretório a ser excluído.
            forcar (bool): Se True, exclui mesmo se o diretório não estiver vazio.

        Raises:
            NotADirectoryError: Se o caminho não for um diretório válido.
            OSError: Se não for possível excluir o diretório.
        """
        diretorio = FolderRepository.buscar_diretorio(caminho)
        if forcar:
            for item in diretorio.caminho.iterdir():
                if item.is_dir():
                    FolderRepository.excluir_diretorio(item, forcar=True)
                else:
                    item.unlink()
        diretorio.caminho.rmdir()

    @staticmethod
    def listar_diretorios_vazios(diretorio: Path) -> List[Diretorio]:
        """
        Lista todos os subdiretórios vazios dentro de um diretório.

        Args:
            diretorio (Path): Caminho do diretório.

        Returns:
            List[Diretorio]: Lista de objetos Diretorio que estão vazios.
        """
        subdiretorios = FolderRepository.listar_subdiretorios(diretorio)
        return [subdir for subdir in subdiretorios if not any(subdir.caminho.iterdir())]

    @staticmethod
    def verificar_existencia_diretorio(caminho: Path) -> bool:
        """
        Verifica se um diretório existe.

        Args:
            caminho (Path): Caminho do diretório a ser verificado.

        Returns:
            bool: True se o diretório existir, False caso contrário.
        """
        return caminho.is_dir()
