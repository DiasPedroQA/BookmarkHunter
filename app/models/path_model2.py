# app/models/path_model.py

"""
Módulo para gerenciar caminhos de arquivos e diretórios.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ItemSistema:
    """Representa um item genérico no sistema de arquivos."""

    def __init__(self, caminho: Path) -> None:
        if not caminho.exists():
            raise ValueError(f"O caminho {caminho} não existe.")
        self._caminho: Path = caminho
        self._nome: str = caminho.name
        self._data_criacao: float = caminho.stat().st_ctime
        self._data_modificacao: float = caminho.stat().st_mtime

    def para_json(self) -> Dict[str, Any]:
        """Retorna as informações básicas do item como um dicionário."""
        return {
            "caminho_absoluto": self.caminho_absoluto(),
            "nome": self._nome,
            "data_criacao": self.formatar_data_brasileira(self._data_criacao),
            "data_modificacao": self.formatar_data_brasileira(self._data_modificacao),
        }

    def caminho_absoluto(self) -> str:
        """Retorna o caminho absoluto do item."""
        return str(self._caminho.resolve())

    @staticmethod
    def formatar_data_brasileira(timestamp: float) -> str:
        """Formata a data para o formato brasileiro (dd/mm/yyyy)."""
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")


class Arquivo(ItemSistema):
    """Representa um arquivo no sistema de arquivos."""

    def __init__(self, caminho: Path) -> None:
        if not caminho.is_file():
            raise ValueError(f"O caminho {caminho} não é um arquivo válido.")
        super().__init__(caminho)
        self.extensao: str = caminho.suffix
        self.tamanho_formatado: str = self._formatar_tamanho_arquivo(caminho.stat().st_size)

    @staticmethod
    def _formatar_tamanho_arquivo(tamanho_arquivo: int) -> str:
        """Formata o tamanho do arquivo para uma string legível."""
        for unidade in ["bytes", "KB", "MB", "GB"]:
            if tamanho_arquivo < 1024:
                return f"{tamanho_arquivo:.2f} {unidade}"
            tamanho_arquivo /= 1024
        return f"{tamanho_arquivo:.2f} TB"

    def para_json(self) -> str:
        """Adiciona informações específicas de arquivo ao JSON."""
        dados = super().para_json()
        dados.update(
            {
                "extensao": self.extensao,
                "tamanho": self.tamanho_formatado,
            }
        )
        return json.dumps(dados, indent=4, ensure_ascii=False)


class Diretorio(ItemSistema):
    """Representa um diretório no sistema de arquivos."""

    def __init__(self, caminho: Path) -> None:
        if not caminho.is_dir():
            raise ValueError(f"O caminho {caminho} não é um diretório válido.")
        super().__init__(caminho)
        self.arquivos: List[Arquivo] = []
        self.subdiretorios: List[Diretorio] = []
        self._atualizar_conteudo()

    def _atualizar_conteudo(self) -> None:
        """Atualiza o conteúdo do diretório."""
        self.arquivos.clear()
        self.subdiretorios.clear()
        for item in self._caminho.iterdir():
            if item.is_file():
                arquivo_valido = Arquivo(item)
                self.arquivos.append(arquivo_valido)
            elif item.is_dir():
                subdiretorio_valido = Diretorio(item)
                self.subdiretorios.append(subdiretorio_valido)

    def para_json(self) -> Dict[str, Any]:
        """Adiciona informações específicas de diretório ao JSON."""
        dados = super().para_json()
        dados.update(
            {
                "sub_arquivos": [arquivo.para_json() for arquivo in self.arquivos],
                "sub_pastas": [subdiretorio.para_json() for subdiretorio in self.subdiretorios],
            }
        )
        return dados

    def buscar_por_extensao(self, extensao: str) -> List[Arquivo]:
        """Busca arquivos dentro do diretório que possuam a extensão fornecida."""
        return [
            arquivo for arquivo in self.arquivos if arquivo.extensao == extensao
        ]
