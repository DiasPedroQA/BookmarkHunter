# app/models/path_model.py

"""
Módulo para análise de caminhos fornecidos, determinando se são absolutos ou relativos,
e se apontam para arquivos ou pastas.

Classes:
    BasePathModel: Classe para análise de caminhos fornecidos, determinando se são absolutos ou relativos,
    e se apontam para arquivos ou pastas.

Métodos:
    __init__: Inicializa uma nova instância da classe BasePathModel e analisa o caminho fornecido.
    _analisar_caminho: Verifica todas as propriedades do caminho utilizando expressões regulares.
    to_dict: Retorna as propriedades do caminho em formato de dicionário.
    montar_objeto: Lê o caminho fornecido e retorna o conteúdo do arquivo.
"""

import json
import re
from typing import Dict, Union, Any
import platform


class BasePathModel:
    """
    Classe para análise de caminhos fornecidos, determinando se são absolutos ou relativos,
    e se apontam para arquivos ou pastas, levando em consideração diferentes sistemas operacionais.
    """

    # Compilando expressões regulares para reutilização
    regex_absoluto_windows = re.compile(r"^[A-Za-z]:\\")
    regex_absoluto_linux = re.compile(r"^/")
    regex_arquivo = re.compile(r"\.([a-zA-Z0-9]+)$")
    regex_termina_com_barra = re.compile(r"/$")

    def __init__(self, caminho_entrada: str) -> None:
        """
        Inicializa uma nova instância da classe BasePathModel e analisa o caminho fornecido.
        """
        self.caminho: str = caminho_entrada
        self.objeto_path: Dict[str, Union[str, Dict[str, str]]] = {}
        self._analisar_caminho()

    def _analisar_caminho(self) -> None:
        """
        Verifica todas as propriedades do caminho utilizando expressões regulares.
        """
        # sistema = platform.system().lower()

        tipo = "Absoluto" if self._eh_absoluto() else "Relativo"
        natureza, extensao, nome, pasta_atual, pasta_mae = self._determinar_natureza()

        # Preenche o dicionário de informações extraídas
        self.objeto_path = {
            "caminho": self.caminho,
            "detalhes": {
                "tipo": tipo,
                "natureza": natureza,
                "extensao": extensao,
            },
            "localizacao": {
                "pasta_mae": pasta_mae,
                "pasta_atual": pasta_atual,
                "nome": nome,
            },
        }

    def _eh_absoluto(self) -> bool:
        """
        Verifica se o caminho é absoluto, dependendo do sistema operacional.
        """
        return (
            bool(self.regex_absoluto_windows.match(self.caminho))
            if platform.system().lower() == "windows"
            else bool(self.regex_absoluto_linux.match(self.caminho))
        )

    def _determinar_natureza(self) -> tuple:
        """
        Determina se o caminho é um arquivo ou uma pasta, extrai as informações relacionadas.
        """
        extensao, nome, pasta_atual, pasta_mae = "", "", "", ""

        if self.regex_arquivo.search(self.caminho):
            natureza = "Arquivo"
            extensao = self.regex_arquivo.search(self.caminho).group(0)
            nome = self.caminho.split(self._get_separator())[-1]
            pasta_atual = self._extrair_pasta(self.caminho)
            pasta_mae = self._extrair_pasta(pasta_atual)
        elif self.regex_termina_com_barra.search(self.caminho):
            natureza = "Pasta"
            pasta_atual = self.caminho.rstrip(self._get_separator())
            nome = pasta_atual.split(self._get_separator())[-1]
            pasta_mae = self._extrair_pasta(pasta_atual)
        else:
            natureza = "Pasta"
            pasta_atual = self.caminho
            nome = pasta_atual.split(self._get_separator())[-1]
            pasta_mae = self._extrair_pasta(pasta_atual)

        return natureza, extensao, nome, pasta_atual, pasta_mae

    def _extrair_pasta(self, caminho: str) -> str:
        """
        Extrai a pasta a partir do caminho.
        """
        return self._get_separator().join(caminho.split(self._get_separator())[:-1])

    def _get_separator(self) -> str:
        """
        Retorna o separador de diretórios apropriado para o sistema operacional atual.
        """
        return "\\" if platform.system().lower() == "windows" else "/"

    @staticmethod
    def remover_vazios(dado: Union[Dict[str, Any], Any]) -> Union[Dict[str, Any], Any]:
        """
        Remove valores nulos, vazios ou strings vazias de um dicionário recursivamente.
        """
        if isinstance(dado, dict):
            return {k: v for k, v in dado.items() if v not in (None, "", [], False)}
        return dado

    def montar_objeto(self) -> str:
        """
        Retorna os dados do objeto BasePathModel no formato JSON.
        """
        # Remove os vazios do dicionário antes de retornar
        dados_limpos: Dict[str, Any] | Any = self.remover_vazios(self.objeto_path)
        return json.dumps(dados_limpos, indent=4, ensure_ascii=False)


# # Exemplo de uso  # pylint: disable=C0103
# if __name__ == "__main__":
#     caminho_teste_pasta_linux = "/home/pedro-pm-dias/Downloads/Chrome/"
#     caminho_teste_arquivo_linux = (
#         "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23__pasta2_2024.html"
#     )

#     # Testando os métodos com a classe
#     caminho_pasta = BasePathModel(caminho_teste_pasta_linux)
#     caminho_arquivo = BasePathModel(caminho_teste_arquivo_linux)

#     print("\nLinux - Pasta:", caminho_pasta.montar_objeto())
#     print("\nLinux - Arquivo:", caminho_arquivo.montar_objeto())

#     # print("\nWindows - Pasta:", caminho_pasta_windows.montar_objeto())
#     # print("\nWindows - Arquivo:", caminho_arquivo_windows.montar_objeto())
