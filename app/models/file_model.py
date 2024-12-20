# app/models/file_model.py

"""
Este módulo define a classe `Arquivo`, que representa um arquivo com atributos como 
nome, caminho, datas de criação e modificação, e um relacionamento com a pasta e 
marcadores associados.

A classe permite associar marcadores ao arquivo e gerenciar suas informações.

Classes:
    - Arquivo: Representa um arquivo com dados e marcadores associados.

Métodos:
    - __init__: Inicializa o objeto Arquivo.
    - add_bookmark: Associa um marcador ao arquivo.
    - __repr__: Retorna uma representação em string do Arquivo.
"""

from typing import Optional
from app.models.folder_model import Pasta


class Arquivo:
    """
    Representa um arquivo com atributos como nome, caminho, datas de criação e
    modificação, pasta mãe e tamanho, além de um relacionamento opcional com a 
    pasta e uma lista de marcadores associados.

    Atributos:
        nome (str): O nome do arquivo.
        caminho (str, opcional): O caminho do arquivo no sistema de arquivos.
        data_criacao (str, opcional): A data de criação do arquivo, em formato de string.
        data_modificacao (str, opcional): A data da última modificação do arquivo, em formato de string.
        pasta_mae (str, opcional): A pasta onde o arquivo está localizado.
        tamanho (int, opcional): O tamanho do arquivo.
        caminho_absoluto (str, opcional): O caminho absoluto do arquivo.
        pasta (Optional["Pasta"], opcional): A pasta associada ao arquivo, caso exista.
        bookmarks (list, opcional): Lista de marcadores associados a este arquivo.
    """

    def __init__(
        self,
        nome: str,
        caminho: Optional[str] = None,
        data_criacao: Optional[str] = None,
        data_modificacao: Optional[str] = None,
        pasta_mae: Optional[str] = None,
        tamanho: Optional[int] = None,
        caminho_absoluto: str = None,
        pasta: Optional["Pasta"] = None,
    ):
        """
        Inicializa um objeto Arquivo.

        Args:
            nome (str): O nome do arquivo.
            caminho (str, opcional): O caminho do arquivo no sistema de arquivos.
            data_criacao (str, opcional): A data de criação do arquivo, em formato de string.
            data_modificacao (str, opcional): A data da última modificação do arquivo, em formato de string.
            pasta_mae (str, opcional): A pasta onde o arquivo está localizado.
            tamanho (int, opcional): O tamanho do arquivo.
            caminho_absoluto (str, opcional): O caminho absoluto do arquivo.
            pasta (Pasta, opcional): A pasta associada ao arquivo, caso exista.
        """
        self.nome = nome
        self.caminho = caminho
        self.data_criacao = data_criacao
        self.data_modificacao = data_modificacao
        self.pasta_mae = pasta_mae
        self.tamanho = tamanho
        self.caminho_absoluto = caminho_absoluto
        self.pasta = pasta  # Relacionamento com a pasta
        self.bookmarks = []  # Lista para armazenar os bookmarks associados

    def add_bookmark(self, marcador):
        """
        Adiciona um marcador à lista de bookmarks do arquivo e cria o relacionamento 
        com o arquivo.

        Args:
            marcador (Marcador): O marcador a ser associado a este arquivo.
        """
        self.bookmarks.append(marcador)
        marcador.arquivo = self

    def __repr__(self) -> str:
        """
        Retorna uma representação em string do objeto Arquivo.

        Returns:
            str: Representação do objeto.
        """
        return f"<Arquivo(nome={self.nome})>"
