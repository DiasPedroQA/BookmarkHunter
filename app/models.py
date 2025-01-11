# pylint: disable=E0401, W0718

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
from os import stat_result
from pathlib import Path
from typing import Union
from services import (
    obter_id_unico,
    obter_dados_caminho,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
    obter_tamanho_arquivo,
    obter_permissoes_caminho,
)
import colorlog  # Para colorir os logs

# Configuração do logger com cores
log_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


class PathModel:
    """
    Classe que representa e manipula um caminho no sistema operacional.

    Atributos:
        caminho_original (str): O caminho inicial fornecido pelo usuário.
        caminho_resolvido (str): O caminho convertido para um formato absoluto.
        existe (bool): Indica se o caminho existe no sistema de arquivos.
        is_arquivo (bool): Indica se o caminho é um arquivo.
        is_diretorio (bool): Indica se o caminho é um diretório.
    """

    def __init__(self, caminho_original: str):
        """
        Inicializa um objeto PathModel.

        Args:
            caminho_original (str): O caminho do sistema de arquivos fornecido pelo usuário.

        Raises:
            ValueError: Se o caminho for vazio ou contiver caracteres inválidos.
        """
        self.caminho_original = caminho_original
        self._validar_caminho(caminho_original)
        self.caminho_resolvido = self._converter_para_absoluto(self.caminho_original)
        self.existe = self._verificar_existencia()
        self.is_arquivo = self._verificar_tipo_caminho("arquivo")
        self.is_diretorio = self._verificar_tipo_caminho("diretorio")
        self.dados_filtrados = obter_dados_caminho(self.caminho_resolvido)

    def _verificar_tipo_caminho(self, tipo: str) -> bool:
        """
        Verifica se o caminho é do tipo especificado (arquivo ou diretório).
        Consolidado em um único método.

        Args:
            tipo (str): O tipo de verificação ('arquivo' ou 'diretorio').

        Returns:
            bool: True se o caminho for do tipo especificado, False caso contrário.
        """
        try:
            path: Path = Path(self.caminho_resolvido)
            if tipo == "arquivo":
                return path.is_file()
            elif tipo == "diretorio":
                return path.is_dir()
            return False
        except OSError as erro:
            logger.error("Erro ao verificar tipo '%s': %s", tipo, erro)
            return False

    def _validar_caminho(self, caminho_atual: str) -> None:
        """
        Valida o caminho fornecido, verificando se não está vazio e não contém caracteres inválidos.

        Args:
            caminho (str): O caminho a ser validado.

        Raises:
            ValueError: Se o caminho for vazio ou contiver caracteres inválidos.
        """
        if not caminho_atual.strip():
            raise ValueError(
                "O caminho não pode ser vazio ou composto apenas por espaços."
            )

        caracteres_invalidos: set[str] = {"?", "*", "|", "<", ">"}
        if any(char in caminho_atual for char in caracteres_invalidos):
            erros = " ".join(caracteres_invalidos)
            raise ValueError(
                f"O caminho contém caracteres inválidos: {erros}"
            )

    def _verificar_existencia(self) -> bool:
        """
        Verifica se o caminho existe no sistema de arquivos.

        Returns:
            bool: True se o caminho existir, False caso contrário.
        """
        try:
            return Path(self.caminho_resolvido).exists()
        except OSError as erro:
            logger.error(
                "Erro ao verificar a existência do caminho '%s': %s", self.caminho_resolvido, erro
            )
            return False

    def _obter_permissoes(self) -> dict[str, bool]:
        """
        Obtém as permissões do caminho resolvido.

        Returns:
            dict[str, bool]: Um dicionário contendo as permissões do caminho.
        """
        try:
            return obter_permissoes_caminho(self.caminho_resolvido)
        except OSError as erro:
            logger.error(
                "Erro ao obter permissões para o caminho '%s': %s", self.caminho_resolvido, erro
            )
            return {"leitura": False, "escrita": False, "execucao": False}

    def _converter_para_absoluto(self, caminho_relativo: str) -> str:
        """
        Converte um caminho relativo para absoluto.

        Args:
            caminho_relativo (str): O caminho a ser processado.

        Returns:
            str: O caminho absoluto resolvido.
        """
        caminho_absoluto: str = str(
            Path(caminho_relativo).resolve()
            if Path(caminho_relativo).is_absolute()
            else Path.home() / caminho_relativo.strip("/")
        )
        return caminho_absoluto

    def _estatisticas_do_caminho(self, caminho_atual: str) -> stat_result:
        """
        Obtém estatísticas detalhadas sobre um caminho.
        """
        try:
            return Path(caminho_atual).stat()
        except FileNotFoundError:
            logger.error("O caminho '%s' não foi encontrado.", caminho_atual)
            raise
        except PermissionError:
            logger.error("Permissão negada ao acessar o caminho '%s'.", caminho_atual)
            raise
        except OSError as erro:
            logger.error("Erro ao acessar o caminho '%s': %s", caminho_atual, erro)
            raise

    def gerar_dados(self) -> dict[str, Union[str, bool]]:
        """
        Gera um dicionário com informações detalhadas sobre o caminho.
        """
        caminho_resolvido = self.caminho_resolvido
        estatisticas = self._estatisticas_do_caminho(caminho_resolvido)
        return {
            "id_caminho": obter_id_unico(identificador=len(caminho_resolvido)),
            "caminho_original": self.caminho_original,
            "caminho_resolvido": caminho_resolvido,
            "existe": self.existe,
            "estatisticas": {
                "data_acesso": obter_data_acesso(estatisticas.st_atime),
                "data_criacao": obter_data_criacao(estatisticas.st_ctime),
                "data_modificacao": obter_data_modificacao(estatisticas.st_mtime),
                "tamanho": obter_tamanho_arquivo(estatisticas.st_size),
            },
            "is_arquivo": self.is_arquivo,
            "is_diretorio": self.is_diretorio,
            "permissoes": self._obter_permissoes(),
            "dados_filtrados": self.dados_filtrados,
        }

    def para_json(self) -> str:
        """
        Converte o objeto PathModel em uma representação JSON.
        """
        return json.dumps(
            self.gerar_dados(), indent=4, ensure_ascii=False, sort_keys=True
        )


# Exemplo de uso
if __name__ == "__main__":
    caminhos = [
        # "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
        # "/home/pedro-pm-dias/Downloads/Chrome/",
        # "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
        "/caminho/inexistente/",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "../../Downloads/Chrome/",
    ]

    for caminho in caminhos:
        try:
            path_obj: PathModel = PathModel(caminho)
            print(path_obj.gerar_dados(), end="\n\n")
        except ValueError as erro:
            logger.warning("Erro de validação para o caminho '%s': %s", caminho, erro)
        except FileNotFoundError:
            logger.warning("O caminho '%s' não foi encontrado.", caminho)
        except PermissionError:
            logger.warning("Permissão negada para o caminho '%s'.", caminho)
        except OSError as erro:
            logger.error("Erro ao processar '%s': %s", caminho, erro)
        except Exception as erro:
            logger.error("Erro inesperado para o caminho '%s': %s", caminho, erro)


# class FileModel(PathModel):
#     """
#     Classe que representa e manipula um arquivo no sistema operacional.
#     """

#     def __init__(self, caminho_original: str):
#         """
#         Inicializa um objeto FileModel a partir de um caminho de arquivo.
#         """
#         super().__init__(caminho_original)

#         if not self.existe:
#             logging.warning("O arquivo '%s' não existe.", self.caminho_resolvido)

#         if not self.is_arquivo:
#             logging.warning(
#                 "O caminho '%s' não é um arquivo válido.", self.caminho_resolvido
#             )

#         self.dados_stat = self._obter_dados_stat() if self.is_arquivo else {}

#     def _obter_dados_stat(self) -> stat_result:
#         """
#         Obtém os dados do método .stat() para o arquivo.

#         Returns:
#             os.stat_result: Objeto contendo as informações detalhadas do arquivo.
#         """
#         try:
#             return Path(self.caminho_resolvido).stat()
#         except FileNotFoundError:
#             logging.error("Arquivo não encontrado: '%s'", self.caminho_resolvido)
#         except OSError as erro:
#             logging.error(
#                 "Erro ao obter informações do arquivo '%s': %s",
#                 self.caminho_resolvido,
#                 erro,
#             )
#         return None

#     def gerar_dados(self) -> dict[str, Union[str, int, bool]]:
#         """
#         Gera um dicionário com informações detalhadas sobre o arquivo.

#         Returns:
#             dict[str, Union[str, int, bool]]: Dados sobre o arquivo.
#         """
#         dados_arquivo = {
#             "caminho_original": self.caminho_original,
#             "caminho_resolvido": self.caminho_resolvido,
#             "caminho_filtrado": self.dados_filtrados,
#             "caminho_existe": self.existe,
#             "caminho_e_arquivo": self.is_arquivo,
#             "caminho_e_diretorio": self.is_diretorio,
#         }

#         if self.dados_stat:
#             dados_arquivo.update(
#                 {
#                     "tamanho_arquivo": obter_tamanho_arquivo(self.dados_stat.st_size),
#                     "ultima_modificacao": obter_data_modificacao(
#                         self.dados_stat.st_mtime
#                     ),
#                     "data_criacao": obter_data_criacao(self.dados_stat.st_ctime),
#                     "ultimo_acesso": obter_data_acesso(self.dados_stat.st_atime),
#                     "permissoes": obter_permissoes_caminho(
#                         self.dados_stat.st_mode & 0o777
#                     ),  # Permissões no estilo Unix
#                     "proprietario_uid": obter_id_unico(self.dados_stat.st_uid),
#                 }
#             )

#         return dados_arquivo


# # Exemplo de uso
# if __name__ == "__main__":
#     caminhos = [
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
#         "/home/pedro-pm-dias/Downloads/Chrome/",
#         "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
#         "/caminho/inexistente/",
#         "../../Downloads/Chrome/favoritos_23_12_2024.html",
#         "../../Downloads/Chrome/favoritos.html",
#         "../../Downloads/Chrome/",
#         "../../Downloads/Chrome/Teste/",
#     ]

#     for caminho in caminhos:
#         file_obj = FileModel(caminho)
#         file_obj_json = file_obj.gerar_dados()
#         print(file_obj_json, end="\n\n")
