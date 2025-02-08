# app/services/global_services.py

"""
Arquivo global dos serviços de manipulação de dados para análises de tags, caminhos, arquivos e diretórios.
"""

from os import stat_result
from pathlib import Path
from datetime import datetime
from typing import Dict, Literal, Union
import platform


class GeneralServices:
    """
    Classe para análise de caminhos de arquivos e diretórios, com métodos para validação,
    sanitização, extração de informações e conversão de dados.
    """

    def __init__(self, caminho_inicial: str) -> None:
        """
        Inicializa a classe com o caminho fornecido.
        """
        self.caminho: Path = Path(caminho_inicial)
        self.caminho_existe: bool = self.caminho.exists()

    @staticmethod
    def _formatar_timestamp(timestamp: float) -> str:
        """
        Formata um timestamp para o formato "dd/mm/aaaa HH:MM:SS".
        """
        return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M:%S")

    @staticmethod
    def _converter_tamanho(tamanho_bytes: int, unidade: str = "auto") -> str:
        """
        Converte o tamanho de bytes para uma unidade legível (KB, MB, GB, TB).
        """
        unidades: list[str] = ["B", "KB", "MB", "GB", "TB"]
        fator_conversao: Literal[1024] = 1024

        if unidade == "auto":
            indice = 0
            while tamanho_bytes >= fator_conversao and indice < len(unidades) - 1:
                tamanho_bytes /= fator_conversao
                indice += 1
            return f"{tamanho_bytes:.2f} {unidades[indice]}"

        if unidade.upper() not in unidades:
            raise ValueError(f"Unidade inválida. Use uma das seguintes: {unidades}")

        indice = unidades.index(unidade.upper())
        tamanho_convertido = tamanho_bytes / (fator_conversao**indice)
        return f"{tamanho_convertido:.2f} {unidades[indice]}"

    def _estatisticas_caminho(self) -> stat_result:
        """
        Retorna as estatísticas do caminho fornecido.
        Levanta FileNotFoundError se o caminho não existir.
        """
        if not self.caminho_existe:
            raise FileNotFoundError("O arquivo ou diretório não existe.")
        return self.caminho.stat()

    def obter_tamanho_formatado(self) -> str:
        """
        Retorna o tamanho do arquivo ou diretório
        formatado em uma unidade legível.
        """
        return self._converter_tamanho(self._estatisticas_caminho().st_size)

    def obter_ultimo_acesso(self) -> str:
        """
        Retorna a data e hora do último acesso ao arquivo ou diretório.
        """
        return self._formatar_timestamp(self._estatisticas_caminho().st_atime)

    def obter_ultima_modificacao(self) -> str:
        """
        Retorna a data e hora da última modificação do arquivo ou diretório.
        """
        return self._formatar_timestamp(self._estatisticas_caminho().st_mtime)

    def obter_data_criacao(self) -> str:
        """
        Retorna a data e hora de criação do arquivo ou diretório.
        """
        return self._formatar_timestamp(self._estatisticas_caminho().st_ctime)

    def obter_permissoes(self) -> str:
        """
        Retorna as permissões do arquivo ou diretório no formato octal.
        """
        return oct(self._estatisticas_caminho().st_mode)

    def obter_sistema_operacional(self) -> str:
        """
        Retorna o nome do sistema operacional.
        """
        return platform.system()

    def obter_metadados(self) -> Dict[str, Union[str, int, float]]:
        """
        Obtém todos os metadados do arquivo ou diretório.
        """
        try:
            estatisticas = self._estatisticas_caminho()
            return {
                "tamanho_formatado": self._converter_tamanho(estatisticas.st_size),
                "ultimo_acesso": self._formatar_timestamp(estatisticas.st_atime),
                "ultima_modificacao": self._formatar_timestamp(estatisticas.st_mtime),
                "data_criacao": self._formatar_timestamp(estatisticas.st_ctime),
                "permissoes": oct(estatisticas.st_mode),
                "sistema_operacional": self.obter_sistema_operacional(),
            }
        except FileNotFoundError as exc:
            raise FileNotFoundError("O arquivo ou diretório não existe.") from exc


if __name__ == "__main__":

    def testar_metodos(caminho_teste: str) -> None:
        # sourcery skip: extract-method
        """
        Testa todos os métodos da classe GeneralServices para um caminho específico.
        """
        print(f"\nAnalisando o caminho: {caminho_teste}")
        analisador = GeneralServices(caminho_teste)

        # Testa cada método individualmente
        try:
            print(f"[Tamanho formatado]: {analisador.obter_tamanho_formatado()}")
            print(f"[Último acesso]: {analisador.obter_ultimo_acesso()}")
            print(f"[Última modificação]: {analisador.obter_ultima_modificacao()}")
            print(f"[Data de criação]: {analisador.obter_data_criacao()}")
            print(f"[Permissões]: {analisador.obter_permissoes()}")
            print(f"[Sistema operacional]: {analisador.obter_sistema_operacional()}")
        except OSError as e:
            print(f"[Erro]: {e}")
        print("-" * 100)

    # Lista de caminhos para teste
    caminhos_teste: list[str] = [
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/arquivo?*<>.html",
        "/home/pedro-pm-dias/Downloads/Chrome/",
        "/home/pedro-pm-dias/Downloads/Chrome/<>/",
        "../Downloads/Chrome/imagens/arquivo?*<>.jpg",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "../../Downloads/Chrome/",
        "../../Downloads/Chrome/<>/",
    ]

    # Testa todos os caminhos na lista
    for caminho in caminhos_teste:
        testar_metodos(caminho)
