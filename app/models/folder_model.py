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

from datetime import datetime
from pathlib import Path
from typing import List
import uuid
from arquivo_model import Arquivo


class Pasta:
    def __init__(self, caminho: str):
        self.pasta_id: str = str(uuid.uuid4())
        self.caminho: Path = Path(caminho).resolve()
        self.nome: str = self.caminho.name
        self.data_criacao: datetime = datetime.fromtimestamp(self.caminho.stat().st_ctime)
        self.data_modificacao: datetime = datetime.fromtimestamp(self.caminho.stat().st_mtime)
        self.arquivos: List['Arquivo'] = []
        self.pastas: List['Pasta'] = []

    def _calcular_tamanho_total(self) -> int:
        return sum(f.stat().st_size for f in self.caminho.rglob('*') if f.is_file())

    def atualizar_conteudo(self):
        self.arquivos = [Arquivo(str(f)) for f in self.caminho.iterdir() if f.is_file()]
        self.pastas = [Pasta(str(p)) for p in self.caminho.iterdir() if p.is_dir()]
    def quantidade_arquivos(self) -> int:
        return len(self.arquivos)

    def quantidade_subpastas(self) -> int:
        return len(self.pastas)
