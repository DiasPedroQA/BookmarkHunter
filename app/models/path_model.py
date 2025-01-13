# pylint: disable=C, R, E, W

"""
Descrição:
    Este módulo define a classe PathModel para validação e manipulação de caminhos
    no sistema de arquivos. Ele utiliza métodos para obter informações detalhadas 
    como tipo, estatísticas, e resolução de links simbólicos e caminhos relativos.

Objetos:
    - PathModel: Representa e manipula um caminho no sistema operacional.

Dependências:
    Este módulo utiliza funções do arquivo 'services.py' para obter informações
    detalhadas sobre caminhos, como estatísticas e permissões.
"""

import logging
from pathlib import Path
from typing import Union, Dict
import json
import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)


from app.services.file_services import obter_tamanho_arquivo
from app.services.path_services import (
    fatiar_caminho,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
)

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class PathModel:
    """
    Classe para validação e manipulação de caminhos do sistema de arquivos.
    """

    def __init__(self, caminho: str):
        """
        Inicializa o modelo com um caminho específico.

        :param caminho: Caminho para validação e manipulação.
        """
        self.caminho: str = caminho

    def validar_caminho(self) -> str:
        """
        Valida o caminho e retorna informações formatadas como JSON.

        :return: Informações detalhadas sobre o caminho em formato JSON.
        """
        path_obj = Path(self.caminho)

        if not self.caminho:
            return self._gerar_resposta_json("Caminho vazio", status="ERROR")

        if path_obj.is_symlink():
            return self._tratar_link_simbolico(path_obj)

        if path_obj.exists():
            return self._tratar_caminho_existente(path_obj)

        if self.caminho.startswith("../"):
            return self._tratar_caminho_relativo()

        return self._gerar_resposta_json(
            f"Caminho '{self.caminho}' não existe.", status="ERROR"
        )

    def _tratar_link_simbolico(self, path_obj: Path) -> str:
        """
        Resolve links simbólicos e retorna informações detalhadas.

        :param path_obj: Objeto Path representando o link simbólico.
        :return: Informações sobre o link simbólico em formato JSON.
        """
        try:
            caminho_resolvido = path_obj.resolve()
            return self._gerar_resposta_json(
                "Link simbólico resolvido com sucesso.",
                caminho_original=self.caminho,
                caminho_resolvido=str(caminho_resolvido),
                tipo=self._determinar_tipo_caminho(caminho_resolvido),
                estatisticas=self._obter_estatisticas(caminho_resolvido),
            )
        except FileNotFoundError:
            return self._gerar_resposta_json(
                "Link simbólico inválido. Destino não encontrado.", status="ERROR"
            )

    def _tratar_caminho_existente(self, path_obj: Path) -> str:
        """
        Trata caminhos existentes e retorna informações detalhadas.

        :param path_obj: Objeto Path representando o caminho.
        :return: Informações sobre o caminho em formato JSON.
        """
        return self._gerar_resposta_json(
            "Caminho válido.",
            caminho_original=self.caminho,
            caminho_resolvido=str(path_obj),
            tipo=self._determinar_tipo_caminho(path_obj),
            estatisticas=self._obter_estatisticas(path_obj),
        )

    def _tratar_caminho_relativo(self) -> str:
        """
        Resolve caminhos relativos para absolutos e valida sua existência.

        :return: Informações sobre o caminho em formato JSON.
        """
        caminho_resolvido = self._converter_para_absoluto(self.caminho)
        path_resolvido = Path(caminho_resolvido)

        if path_resolvido.exists():
            return self._gerar_resposta_json(
                mensagem="Caminho relativo resolvido e válido.",
                caminho_original=self.caminho,
                caminho_resolvido=str(path_resolvido),
                tipo=self._determinar_tipo_caminho(path_resolvido),
                estatisticas=self._obter_estatisticas(path_resolvido),
            )

        return self._gerar_resposta_json(
            f"Caminho relativo '{self.caminho}' é inválido.", status="ERROR"
        )

    def _obter_estatisticas(self, path_obj: Path) -> Dict[str, Union[str, int]]:
        """
        Obtém estatísticas detalhadas sobre um caminho existente.

        :param path_obj: Objeto Path do caminho.
        :return: Dicionário com estatísticas do caminho.
        """
        try:
            stats = path_obj.stat()
            return {
                "data_acesso": obter_data_acesso(stats.st_atime),
                "data_criacao": obter_data_criacao(stats.st_ctime),
                "data_modificacao": obter_data_modificacao(stats.st_mtime),
                "tamanho": obter_tamanho_arquivo(stats.st_size),
            }
        except FileNotFoundError:
            logging.error(f"Estatísticas não encontradas para '{path_obj}'.")
            return {
                "data_acesso": "",
                "data_criacao": "",
                "data_modificacao": "",
                "tamanho": "",
            }

    def _converter_para_absoluto(self, caminho_relativo: str) -> str:
        """
        Converte um caminho relativo para um caminho absoluto.

        :param caminho_relativo: Caminho relativo.
        :return: Caminho absoluto como string.
        """
        return str((Path.home() / Path(caminho_relativo.lstrip("../"))).resolve())

    def _determinar_tipo_caminho(self, path_obj: Path) -> str:
        """
        Determina o tipo de um caminho (Arquivo, Diretório ou Inválido).

        :param path_obj: Objeto Path do caminho.
        :return: Tipo do caminho como string.
        """
        if path_obj.is_file():
            return "Arquivo"
        if path_obj.is_dir():
            return "Diretório"
        return "Inválido"

    def _gerar_resposta_json(
        self,
        mensagem: str,
        status: str = "OK",
        **dados_caminho: Union[str, Dict[str, Union[str, int]]],
    ) -> str:
        """
        Gera uma resposta formatada em JSON.

        :param mensagem: Mensagem descritiva do resultado.
        :param status: Status do resultado (OK, ERROR, etc.).
        :param dados_caminho: Dados adicionais a serem incluídos.
        :return: Resposta formatada como JSON.
        """
        resposta = {
            "mensagem": mensagem,
            "status": status,
            "dados_caminho": dados_caminho,
        }
        return json.dumps(resposta, indent=4, ensure_ascii=False)


# # Exemplo de uso:
# caminhos_para_validar: list[str] = [
#     "/caminho/inexistente/",
#     "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#     "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
#     "/home/pedro-pm-dias/Downloads/Chrome/",
#     "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#     "../../Downloads/Chrome/favoritos.html",
#     "../../Downloads/Chrome/favoritos_23_12_2024.html",
#     "../../Downloads/Chrome/",
#     "../../Downloads/Chrome/Teste/",
#     "/home/pedro-pm-dias/Downloads/Chrome/favoritos_link_simbólico",  # Exemplo de link simbólico
# ]

# for caminho in caminhos_para_validar:
#     modelo = PathModel(caminho)
#     print("\n", modelo.validar_caminho())
