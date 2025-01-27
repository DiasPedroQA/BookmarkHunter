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
        self.caminho_validado = self.validar_e_sanitizar_caminho(caminho_inicial)

    @staticmethod
    def validar_e_sanitizar_caminho(caminho: str) -> str:
        """Valida e sanitiza o caminho fornecido."""
        # Validação do caminho
        if not isinstance(caminho, str) or not caminho.strip():
            raise ValueError("O caminho deve ser uma string não vazia.")
        if len(caminho) > 260:
            raise ValueError("O caminho excede o limite de 260 caracteres.")

        # Sanitização do caminho
        caminho_normalizado = re.sub(r"[\\/]+", "/", caminho.strip())
        return re.sub(r"[^a-zA-Z0-9:\- _./]", "", caminho_normalizado)

    @staticmethod
    def verificar_tipo_caminho(caminho: str) -> Dict[str, bool]:
        """
        Verifica se o caminho é absoluto, relativo, representa um arquivo ou uma pasta.
        """
        # Limpa espaços indesejados
        caminho = caminho.strip()

        # Verificar se é absoluto ou relativo
        e_absoluto = bool(re.match(r"^(?:[a-zA-Z]:\\|/)", caminho))
        e_relativo = bool(re.match(r"^(?:\.{1,2}[\\/])", caminho))

        # Fatiar o caminho e verificar o último elemento
        partes = caminho.strip("/\\").split("/")
        ultimo_elemento = partes[-1] if partes else ""

        # Identificar arquivo com base na extensão
        e_arquivo = bool(re.search(r"\.", ultimo_elemento)) and not caminho.endswith(
            "/"
        )

        # Identificar pasta (se não for arquivo, é pasta)
        e_pasta = not e_arquivo

        return {
            "absoluto": e_absoluto,
            "relativo": e_relativo,
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
        return partes[-2] if len(partes) >= 2 else None

    @staticmethod
    def contar_diretorios(caminho: str) -> int:
        """
        Conta o número de diretórios no caminho fornecido,
        desconsiderando as barras extras no início e no final.
        Também considera se o caminho é de arquivo ou pasta.
        """
        # Remover as barras no início e no final do caminho
        caminho = caminho.strip("/\\")

        # Se o caminho estiver vazio após o strip, retornamos 0
        if not caminho:
            return 0

        # Separar os diretórios pela barra "/"
        partes = caminho.split("/")

        # Se a última parte é um arquivo (presença de um ponto), não contamos como diretório
        return len(partes) - 1 if "." in partes[-1] else len(partes)

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


if __name__ == "__main__":
    # Dicionário de tipos de caminhos para teste
    tipos_de_caminhos: Dict[str, str] = {
        "Arquivo - Absoluto e válido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "Arquivo - Relativo e válido": "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "Arquivo - Absoluto e inválido": "/home/pedro-pm-dias/Downloads/Chrome/arquivo?*<>.html",
        "Arquivo - Relativo e inválido": "../Downloads/Chrome/imagens/arquivo?*<>.jpg",
        "Pasta - Absoluta e válida": "/home/pedro-pm-dias/Downloads/Chrome/",
        "Pasta - Relativa e válida": "../../Downloads/Chrome/",
        "Pasta - Absoluta e inválida": "/home/pedro-pm-dias/Downloads/Chrome/<>/",
        "Pasta - Relativa e inválida": "../../Downloads/Chrome/<>/",
    }

    for descricao, caminho_teste in tipos_de_caminhos.items():
        print(f"\n[Descrição do Caminho]: {descricao}")
        print(f"[Caminho]: {caminho_teste}")
        analisador = RegexPathAnalyzer(caminho_inicial=caminho_teste)
        resultado = analisador.extrair_pasta_principal(caminho=caminho_teste)
        #         resultado = analisador.analisar_caminho()
        #         for chave, valor in resultado.items():
        #             print(f"  - {chave.replace('_', ' ').capitalize()}: {valor}")
        print(f"  - {resultado}")
