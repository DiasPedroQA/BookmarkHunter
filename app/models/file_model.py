# app/models/file_model.py
# pylint: disable=E, C, W

"""
Módulo para processar arquivos e extrair informações relevantes.
Este módulo fornece a classe ObjetoArquivo para obter informações detalhadas sobre arquivos.

Classes:
    ObjetoArquivo: Classe para obter informações detalhadas sobre arquivos.
"""

import os
import sys
import json
from typing import Dict, Optional, Union
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.models import BasePathModel, ObjetoTag  # Importa a classe base
from app.utils import ConversoresUtils, GeradoresUtils


class ObjetoArquivo(BasePathModel):
    """
    Classe para obter informações detalhadas sobre arquivos.
    Herda da classe BasePathModel para análise de caminhos e expande com métodos para processar arquivos.
    """

    EXTENSOES_SUPORTADOS = [".html", ".htm", ".txt"]  # Tipos de arquivos suportados

    def __init__(self, caminho_atual: str):
        """
        Inicializa a classe ObjetoArquivo e configura o caminho do arquivo.
        Chama o construtor da classe base para analisar o caminho.
        """
        super().__init__(
            caminho_atual
        )  # Chama o construtor da classe base para analisar o caminho
        self.path_obj = Path(
            caminho_atual
        )  # Cria um objeto Path para manipulação adicional
        self.conversores = ConversoresUtils()
        self.geradores: GeradoresUtils = GeradoresUtils()
        self.objeto_tag: Optional[ObjetoTag] = None

    def ler_caminho_arquivo(self) -> str:
        """
        Lê o conteúdo do arquivo, se for um arquivo.
        """
        if self.objeto_path["detalhes"]["natureza"] == "Arquivo":
            with self.path_obj.open("r", encoding="utf-8") as arquivo:
                return arquivo.read()
        else:
            raise ValueError(f"O caminho {self.caminho} não é um arquivo.")

    def calcular_estatisticas(self, conteudo: str) -> Dict[str, Dict[str, int]]:
        """
        Calcula estatísticas do conteúdo do arquivo.

        Args:
            conteudo (str): Conteúdo do arquivo.

        Returns:
            dict: Estatísticas como número de linhas, palavras e caracteres.
        """
        linhas: list[str] = conteudo.splitlines()
        return {
            "estatisticas": {
                "linhas": len(linhas),
                "palavras": sum(len(linha.split()) for linha in linhas),
                "caracteres": len(conteudo),
            }
        }

    def obter_informacoes_path(self) -> Dict[str, Union[bool, str]]:
        """
        Obtém informações adicionais sobre o caminho usando pathlib.

        Returns:
            dict: Informações detalhadas sobre o caminho.
        """
        if not self.path_obj.exists():
            return {"existe": False}

        stats: os.stat_result = self.path_obj.stat()
        return {
            "existe": True,
            "tamanho": self.conversores.converter_tamanho_arquivo(stats.st_size),
            "modificado_em": self.conversores.converter_timestamp_para_data_hora_br(stats.st_mtime),
            "criado_em": self.conversores.converter_timestamp_para_data_hora_br(stats.st_ctime),
            "acessado_em": self.conversores.converter_timestamp_para_data_hora_br(stats.st_atime),
        }

    def montar_objeto(self) -> dict:
        """
        Retorna as propriedades da classe em formato de dicionário,
        combinando as informações da classe base com os dados adicionais.

        Returns:
            dict: Dados combinados da classe base e informações adicionais.
        """
        base_path_data: Dict = json.loads(
            super().ler_caminho()
        )  # Obtém os dados da classe base

        if self.path_obj.is_file():
            conteudo: str = self.ler_caminho_arquivo()
            estatisticas: Dict[str, Dict[str, int]] = self.calcular_estatisticas(conteudo)
            base_path_data.update(estatisticas)

        base_path_data["path_info"] = self.obter_informacoes_path()
        return base_path_data


# Testando a classe ObjetoArquivo
if __name__ == "__main__":
    caminho_teste_arquivo = (
        "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html"
    )
    objeto_arquivo = ObjetoArquivo(caminho_teste_arquivo)
    print("\nDados de um arquivo existente:")
    dados_arquivo = objeto_arquivo.to_dict()  # Exibe os dados do arquivo em formato JSON
    for k, v in dados_arquivo.items():
        print(f"\n{k}: {v}")

    # caminho_teste_arquivo = (
    #     "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_25_12_2024.html"
    # )
    # objeto_arquivo = ObjetoArquivo(caminho_teste_arquivo)
    # print("\nDados de um arquivo não existente:")
    # pprint(objeto_arquivo.to_dict())  # Exibe os dados do arquivo em formato JSON


# class ObjetoArquivo(BasePathModel, ObjetoTag):
#     """
#     Classe para obter informações detalhadas sobre arquivos.
#     """

