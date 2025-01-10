# app/repositories/file_repository.py
# pylint: disable=E0401

"""
Repositório para manipulação de arquivos e diretórios (versão virtualizada).
"""

import json
from pathlib import Path
from typing import List, Union
from models import Arquivo, Diretorio
from repositories.path_repository import PathRepository


class FileRepository(PathRepository):
    """
    Repositório para manipulação virtual de arquivos e diretórios,
    estendendo funcionalidades de manipulação de caminhos do PathRepository.
    """

    arquivos_virtuais: List[Arquivo] = []
    diretorios_virtuais: List[Diretorio] = []

    @staticmethod
    def buscar_arquivo(caminho: Path) -> Union[Arquivo, None]:
        """
        Busca um arquivo na lista de arquivos virtuais.

        Args:
            caminho (Path): Caminho do arquivo a ser buscado.

        Returns:
            Union[Arquivo, None]: Objeto Arquivo se encontrado, None caso contrário.
        """
        caminho = PathRepository.ajustar_caminhos(
            caminho
        )  # Reutiliza método do PathRepository
        return next(
            (
                arquivo
                for arquivo in FileRepository.arquivos_virtuais
                if arquivo.caminho == caminho
            ),
            None,
        )

    @staticmethod
    def buscar_diretorio(caminho: Path) -> Union[Diretorio, None]:
        """
        Busca um diretório na lista de diretórios virtuais.

        Args:
            caminho (Path): Caminho do diretório a ser buscado.

        Returns:
            Union[Diretorio, None]: Objeto Diretorio se encontrado, None caso contrário.
        """
        caminho = PathRepository.ajustar_caminhos(
            caminho
        )  # Reutiliza método do PathRepository
        return next(
            (
                diretorio
                for diretorio in FileRepository.diretorios_virtuais
                if diretorio.caminho == caminho
            ),
            None,
        )

    @staticmethod
    def listar_arquivos(diretorio_atual: Path) -> List[Arquivo]:
        """
        Lista todos os arquivos dentro de um diretório virtual.

        Args:
            diretorio_atual (Path): Caminho do diretório.

        Returns:
            List[Arquivo]: Lista de objetos Arquivo no diretório especificado.
        """
        diretorio_atual = PathRepository.validar_diretorio(
            diretorio_atual
        )  # Reutiliza validação do PathRepository
        return [
            arquivo
            for arquivo in FileRepository.arquivos_virtuais
            if arquivo.caminho.parent == diretorio_atual
        ]

    @staticmethod
    def listar_arquivos_por_extensao(
        diretorio_atual: Path, extensoes: List[str]
    ) -> List[Arquivo]:
        """
        Lista arquivos em um diretório virtual com extensões específicas.

        Args:
            diretorio_atual (Path): Diretório de onde listar os arquivos.
            extensoes (List[str]): Lista de extensões desejadas (e.g., [".txt", ".json"]).

        Returns:
            List[Arquivo]: Lista de objetos Arquivo com as extensões desejadas.
        """
        diretorio_atual = PathRepository.validar_diretorio(diretorio_atual)
        extensoes = [ext.lower() for ext in extensoes]
        return [
            arquivo
            for arquivo in FileRepository.arquivos_virtuais
            if arquivo.caminho.parent == diretorio_atual
            and arquivo.caminho.suffix.lower() in extensoes
        ]

    @staticmethod
    def salvar_analise(analise, diretorio_saida: Path) -> None:
        """
        Simula o salvamento da análise em um arquivo JSON na lista virtual.

        Args:
            analise: Objeto de análise contendo dados para salvar.
            diretorio_saida (Path): Caminho de saída para o arquivo JSON.
        """
        diretorio_saida = PathRepository.validar_diretorio(
            diretorio_saida
        )  # Valida o diretório
        print(f"Salvando análise em: {diretorio_saida / f'{analise.file}.json'}")
        print(json.dumps(analise.to_dict(), indent=4))
