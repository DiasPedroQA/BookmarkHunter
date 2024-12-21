# app/models/folder_model.py
# pylint: disable=C

"""
Este módulo define a classe `Pasta`, que representa uma pasta contendo arquivos e 
subpastas, com atributos como nome e pasta mãe. A classe permite associar arquivos 
e subpastas à pasta.

Classes:
    - Pasta: Representa uma pasta com arquivos e subpastas associadas.

Métodos:
    - __init__: Inicializa o objeto Pasta.
    - add_arquivo: Associa um arquivo à pasta.
    - __repr__: Retorna uma representação em string da Pasta.
"""

class Pasta:
    def __init__(self, name, pasta_mae):
        """
        Inicializa o objeto Pasta.

        Args:
            name (str): O nome da pasta.
            pasta_mae (Pasta): A pasta mãe que contém essa pasta.
        """
        self.name = name
        self.pasta_mae = pasta_mae
        self.pastas = []  # Lista para armazenar subpastas
        self.arquivos = []  # Lista para armazenar os arquivos associados

    def add_arquivo(self, arquivo):
        """
        Associa um arquivo à pasta.

        Args:
            arquivo (Arquivo): O arquivo a ser associado à pasta.
        """
        self.arquivos.append(arquivo)
        arquivo.pasta = self

    def __repr__(self):
        """
        Retorna uma representação em string da pasta.

        Returns:
            str: Representação da pasta.
        """
        return f"<Pasta(name={self.name})>"
