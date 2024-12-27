# app/models/file_model.py

"""
Módulo para processar arquivos e extrair informações relevantes.
Este módulo fornece a classe ObjetoArquivo para obter informações detalhadas sobre arquivos.

Classes:
    ObjetoArquivo: Classe para obter informações detalhadas sobre arquivos.
"""

import os
import sys
from pathlib import Path
import platform
from typing import Dict, Optional, List
from bs4 import BeautifulSoup

# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C, W0212, W0621
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.models.bookmark_model import ObjetoTag, TagConfig
from app.utils.conversores import ConversoresUtils
from app.utils.geradores import GeradoresUtils


class FileData(Dict):
    """
    Estrutura para representar dados de arquivos processados.
    """

    id_arquivo: str
    sistema_operacional: str
    caminho_absoluto: str
    nome_arquivo: str
    extensao_arquivo: str
    is_file: bool
    is_dir: bool
    tamanho_arquivo: Optional[str]
    data_criacao: Optional[str]
    data_modificacao: Optional[str]


# Classe para configurar os arquivos
class FileConfig:
    """
    Configurações para o processamento de arquivos.
    """

    SUPORTADOS = [".html", ".htm", ".txt"]  # Tipos de arquivos suportados

    def __str__(self) -> str:
        return f"FileConfig(SUPORTADOS={self.SUPORTADOS})"


class ObjetoArquivo(ObjetoTag):
    """
    Processa arquivos para extrair informações estruturadas e realizar operações auxiliares.
    A classe herda de ObjetoTag para reutilizar a lógica de processamento de tags.
    """

    def __init__(
        self,
        caminho: str,
        conversores=ConversoresUtils(),
        geradores=GeradoresUtils(),
        file_config=FileConfig(),
        tag_config=TagConfig(),
    ):
        # Chama o construtor da classe base ObjetoTag
        super().__init__(html="", conversores=conversores, geradores=geradores)

        self.caminho_atual = Path(caminho)
        self.conversores = conversores
        self.geradores = geradores
        self.config_file = file_config
        self.config_tag = tag_config
        self.tags_ignoradas: List[str] = []  # Para armazenar as tags ignoradas

        if self._verificar_existencia:
            self._stat = self.caminho_atual.stat()
            self._tamanho_arquivo = self.conversores.converter_tamanho_arquivo(
                self._stat.st_size
            )
            self._datas_arquivo = {
                "data_criacao": self.conversores.converter_timestamp_para_data_br(
                    self._stat.st_ctime
                ),
                "data_modificacao": self.conversores.converter_timestamp_para_data_br(
                    self._stat.st_mtime
                ),
            }
        else:
            self._stat = None
            self._tamanho_arquivo = None
            self._datas_arquivo = {}

    @property
    def _verificar_existencia(self) -> bool:
        """
        Verifica se o arquivo ou diretório existe.
        """
        return self.caminho_atual.exists()

    def informacoes_arquivo(self) -> FileData:
        """
        Obtém informações detalhadas sobre o arquivo ou diretório.
        """
        if not self._verificar_existencia:
            return {"erro": "Arquivo ou diretório não encontrado."}
        return {
            "id_arquivo": self.geradores.gerar_id(),
            "sistema_operacional": platform.system(),
            "caminho_absoluto": str(self.caminho_atual.resolve()),
            "nome_arquivo": self.caminho_atual.name,
            "extensao_arquivo": self.caminho_atual.suffix,
            "is_file": self.caminho_atual.is_file(),
            "is_dir": self.caminho_atual.is_dir(),
            "tamanho_arquivo": self._tamanho_arquivo,
            **self._datas_arquivo,
        }

    def _ler_arquivo(self) -> Optional[str]:
        """
        Lê o conteúdo de um arquivo se ele existir.
        """
        if not self.caminho_atual.is_file():
            return None
        try:
            with open(self.caminho_atual, "r", encoding="utf-8") as file:
                return file.read()
        except (FileNotFoundError, PermissionError, OSError):
            return None

    def _processar_html(self, html_conteudo: str) -> Dict[str, str]:
        """
        Processa as tags do conteúdo HTML e retorna as tags válidas e inválidas.
        """
        soup = BeautifulSoup(html_conteudo, "html.parser")
        tags_validas = []
        tags_invalidas = []

        # Conta as tags válidas
        for tag in soup.find_all():
            if tag.name in self.config_tag.TAGS_ALVO:  # Somente tags de interesse
                if self._validar_tag(tag):  # Verifica se é uma tag válida
                    tags_validas.append(self._objeto_tag(tag))  # Adiciona tags válidas
                else:
                    tags_invalidas.append(tag.name)  # Adiciona tags inválidas

        # Conta as tags e prepara o resumo
        total_tags_validas = len(tags_validas)
        total_tags_invalidas = len(tags_invalidas)

        print(f"Tags Válidas: {total_tags_validas}")
        print(f"Tags Inválidas: {total_tags_invalidas}")

        return {
            "tags_validas": tags_validas,
            "total_tags_validas": total_tags_validas,
            "tags_invalidas": tags_invalidas,
            "total_tags_invalidas": total_tags_invalidas,
        }

    def processar_tags_arquivo(self) -> Optional[Dict[str, str]]:
        """
        Processa o conteúdo do arquivo e extrai informações relevantes como tags.
        """
        arquivo_conteudo = self._ler_arquivo()  # Lê o conteúdo do arquivo
        if (
            not arquivo_conteudo
            or self.caminho_atual.suffix.lower() not in self.config_file.SUPORTADOS
        ):
            return None

        # Agora passamos o conteúdo HTML corretamente para o método _processar_html
        tags_processadas = self._processar_html(arquivo_conteudo)

        # Retorna as tags válidas processadas e o resumo
        return tags_processadas

    def resumo_processamento(self) -> Dict[str, int]:
        """Retorna um resumo do processamento com contagem de tags analisadas e ignoradas."""
        # Extrai tags processadas de uma vez
        tags_info = self.processar_tags_arquivo()
        if not tags_info:
            return {"erro": "Não foi possível processar o arquivo."}

        return {
            "total_tags_validas": tags_info["quant_tags_validas"],  # Tags válidas
            "total_tags_ignoradas": tags_info["quant_tags_ignoradas"],  # Tags ignoradas
        }


# Exemplo de uso:
if __name__ == "__main__":
    caminho_arquivo = (
        "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html"
    )
    obj_arquivo = ObjetoArquivo(caminho_arquivo)

    # Exibir informações do arquivo
    informacoes: FileData = obj_arquivo.informacoes_arquivo()
    if isinstance(informacoes, dict) and "erro" not in informacoes:
        print("Informações do Arquivo:")
        for chave, valor in informacoes.items():
            print(f"{chave}: {valor}")
    else:
        print(informacoes["erro"])

    # Processar conteúdo do arquivo
    tags_info: Dict[str, str] | None = obj_arquivo.processar_tags_arquivo()
    if tags_info:
        print("\nInformações Processadas:")
        print(f"Título do Arquivo: {tags_info['titulo_arquivo']}")
        print(f"Quantidade de tags válidas <a>: {tags_info['quant_tags_validas']}")
        print(f"Quantidade de tags inválidas: {tags_info['quant_tags_ignoradas']}")
    else:
        print("\nNão foi possível processar as tags do arquivo.")

    # Resumo do processamento
    resumo: Dict[str, int] = obj_arquivo.resumo_processamento()
    print("\nResumo de Tags Processadas:")
    print(resumo)
