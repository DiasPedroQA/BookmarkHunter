# app/services/path_services.py
# pylint: disable=C0114

import re
from typing import Dict, Union, Optional


class RegexPathAnalyzer:
    """
    Classe para análise de informações sobre caminhos de arquivos e diretórios
    utilizando expressões regulares e manipulação de strings.
    """

    def __init__(self, caminho_inicial: str):
        self.caminho_validado = self.validar_caminho(caminho_inicial)

    @staticmethod
    def sanitizar_caminho(caminho_para_sanitizar: str) -> str:
        """Remove caracteres inválidos do caminho e normaliza-o."""
        caminho_normalizado = re.sub(r"[\\/]+", "/", caminho_para_sanitizar.strip())
        return re.sub(r"[^a-zA-Z0-9\- _./]", "", caminho_normalizado)

    @staticmethod
    def validar_caminho(caminho: str) -> str:
        """Valida um caminho fornecido e retorna o caminho sanitizado."""
        if not isinstance(caminho, str) or not caminho.strip():
            raise ValueError("O caminho deve ser uma string não vazia.")
        if len(caminho) > 260:
            raise ValueError("O caminho excede o limite de 260 caracteres.")
        return RegexPathAnalyzer.sanitizar_caminho(caminho)

    @staticmethod
    def verificar_tipo_caminho(caminho: str) -> Dict[str, bool]:
        """Verifica se o caminho é absoluto, relativo, representa um arquivo ou uma pasta."""
        e_arquivo = bool(re.search(r"\.[a-zA-Z0-9]+$", caminho))
        e_pasta = not e_arquivo and caminho.endswith("/")
        return {
            "absoluto": bool(re.match(r"^(?:[a-zA-Z]:\\|/)", caminho)),
            "relativo": bool(re.match(r"^(?:\.{1,2}/)", caminho)),
            "arquivo": e_arquivo,
            "pasta": e_pasta,
        }

    @staticmethod
    def extrair_pasta_principal(caminho: str) -> Optional[str]:
        """
        Extrai a pasta principal do caminho fornecido.
        Para caminhos relativos que começam com '../', retorna None.
        """
        partes = caminho.strip("/\\").split("/")
        return partes[-2] if partes else None

    @staticmethod
    def contar_diretorios(caminho: str) -> int:
        """Conta o número de diretórios no caminho fornecido."""
        return caminho.strip("/\\").count("/")

    def analisar_caminho(self) -> Dict[str, Union[str, bool, int, None]]:
        """
        Realiza a análise completa do caminho e retorna um dicionário com os resultados.
        Aproveita os resultados de métodos auxiliares para evitar cálculos duplicados.
        """
        tipo_caminho = self.verificar_tipo_caminho(self.caminho_validado)
        dados_caminho = {
            "caminho_original": self.caminho_validado,
            "pasta_principal": self.extrair_pasta_principal(self.caminho_validado),
            "numero_diretorios": self.contar_diretorios(self.caminho_validado),
        }
        dados_caminho |= tipo_caminho
        return dados_caminho


# if __name__ == "__main__":
#     # Dicionário de tipos de caminhos para teste
#     tipos_de_caminhos: Dict[str, str] = {
#         "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "Arquivo - Relativo e válido": "../../Downloads/Chrome/favoritos_23_12_2024.html",
#         "Arquivo - Absoluto e inválido": "/home/pedro-pm-dias/Downloads/Chrome/arquivo?*<>.html",
#         "Arquivo - Relativo e inválido": "../Downloads/Chrome/imagens/arquivo?*<>.jpg",
#         "Pasta - Absoluta e válida": "/home/pedro-pm-dias/Downloads/Chrome/",
#         "Pasta - Relativa e válida": "../../Downloads/Chrome/",
#         "Pasta - Absoluta e inválida": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
#         "Pasta - Relativa e inválida": "../../Downloads/Chrome/<>/",
#     }

#     for descricao, caminho_teste in tipos_de_caminhos.items():
#         print(f"\n[Descrição do Caminho]: {descricao}")
#         analisador = RegexPathAnalyzer(caminho_teste)
#         resultado = analisador.analisar_caminho()
#         for chave, valor in resultado.items():
#             print(f"  - {chave.replace('_', ' ').capitalize()}: {valor}")
