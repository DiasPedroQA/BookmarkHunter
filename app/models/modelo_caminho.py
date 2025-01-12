# pylint: disable=E0401, E0611, W0718

"""
Descrição dos modelos de dados utilizados na aplicação.

Objetos:
    - PathModel: Representa e manipula um caminho no sistema operacional.

Dependências:
    Este módulo utiliza funções do arquivo 'services.py' para obter informações
    detalhadas sobre caminhos, como estatísticas e permissões.
"""

import json
import logging
from pathlib import Path
from typing import Union
from app.services.file_services import obter_tamanho_arquivo
from app.services.path_services import (
    obter_id_unico,
    obter_dados_caminho,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
    obter_permissoes_caminho,
    sanitizar_caminho_relativo,
)

# Configuração do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
)
logger.addHandler(console_handler)


class PathModel:
    """
    Classe que representa e manipula um caminho no sistema operacional.
    """

    def __init__(self, caminho_original: str):
        """
        Inicializa um objeto PathModel.

        Args:
            caminho_original (str): O caminho fornecido pelo usuário.

        Raises:
            ValueError: Se o caminho for vazio ou contiver caracteres inválidos.
        """
        self.caminho_original = caminho_original.strip()
        self._validar_entrada()
        self.caminho_resolvido = self._converter_para_absoluto(self.caminho_original)
        self.caminho_existe = Path(self.caminho_resolvido).exists()

        # Se o caminho não existir, configura atributos padrão e loga um aviso.
        if not self.caminho_existe:
            logger.warning("O caminho '%s' não existe.", self.caminho_resolvido)
            self.is_arquivo = False
            self.is_diretorio = False
            self.dados_filtrados = {}
            return

        # Determinar tipo e obter dados se o caminho existir.
        caminho_obj = Path(self.caminho_resolvido)
        self.is_arquivo = caminho_obj.is_file()
        self.is_diretorio = caminho_obj.is_dir()
        self.dados_filtrados = obter_dados_caminho(self.caminho_resolvido)
        self.permissoes_caminho = self._obter_permissoes()

    def _validar_entrada(self) -> None:
        """
        Valida o caminho fornecido pelo usuário.
        """
        if not self.caminho_original:
            raise ValueError("O caminho não pode ser vazio.")
        caracteres_invalidos = {"?", "*", "|", "<", ">"}
        if any(char in self.caminho_original for char in caracteres_invalidos):
            raise ValueError(
                f"O caminho contém caracteres inválidos: {', '.join(caracteres_invalidos)}"
            )

    def _converter_para_absoluto(self, caminho_atual: str) -> str:
        """
        Converte um caminho relativo para absoluto.
        """
        if not Path(caminho_atual).is_absolute():
            caminho_absoluto = f"{Path.home()}/{sanitizar_caminho_relativo(caminho_atual)}"
            return caminho_absoluto
        return caminho_atual

    def _obter_estatisticas(self) -> dict[str, Union[str, int]]:
        """
        Obtém estatísticas do caminho, se ele existir.
        """
        try:
            stats = Path(self.caminho_resolvido).stat()
            return {
                "data_acesso": obter_data_acesso(stats.st_atime),
                "data_criacao": obter_data_criacao(stats.st_ctime),
                "data_modificacao": obter_data_modificacao(stats.st_mtime),
                "tamanho": obter_tamanho_arquivo(stats.st_size),
            }
        except FileNotFoundError:
            logger.error(
                "Estatísticas não encontradas para '%s'.", self.caminho_resolvido
            )
            return {}

    def _obter_permissoes(self) -> dict[str, bool]:
        """
        Obtém as permissões do caminho resolvido.
        """
        try:
            return obter_permissoes_caminho(self.caminho_resolvido)
        except OSError as erro:
            logger.error("Erro ao obter permissões: %s", erro)
            return {"leitura": False, "escrita": False, "execucao": False}

    def gerar_dados(self) -> dict[str, Union[str, bool, dict]]:
        """
        Gera um dicionário com informações detalhadas sobre o caminho.
        """
        if not self.caminho_existe:
            return {
                "caminho_original": self.caminho_original,
                "caminho_resolvido": self.caminho_resolvido,
                "caminho_existe": False,
                "mensagem": "Caminho inexistente.",
            }

        return {
            "id_caminho": obter_id_unico(identificador=len(self.caminho_resolvido)),
            "caminho_original": self.caminho_original,
            "caminho_resolvido": self.caminho_resolvido,
            "caminho_existe": self.caminho_existe,
            "estatisticas": self._obter_estatisticas(),
            "is_arquivo": self.is_arquivo,
            "is_diretorio": self.is_diretorio,
            "permissoes": self.permissoes_caminho,
            "dados_filtrados": self.dados_filtrados,
        }

    def para_json(self) -> str:
        """
        Converte o objeto PathModel em uma representação JSON.
        """
        return json.dumps(
            self.gerar_dados(), indent=4, ensure_ascii=False, sort_keys=True
        )


# # Exemplo de uso
# if __name__ == "__main__":
#     caminhos = [
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/",
#         "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#         "../../Downloads/Chrome/favoritos.html",
#         "/caminho/inexistente/",
#         "../../Downloads/Chrome/favoritos_23_12_2024.html",
#         "../../Downloads/Chrome/",
#         "../../Downloads/Chrome/Teste/",
#     ]

#     for caminho in caminhos:
#         path_obj: PathModel = PathModel(caminho)
#         print('\n', path_obj.gerar_dados(), end="\n\n")
