# pylint: disable=E0401

"""
Descrição dos modelos de dados utilizados na aplicação.

Objetos:
    - PathModel: Representa e manipula um caminho no sistema operacional.
"""


import logging
import os
from pathlib import Path
import json
from typing import Union
from services import (
    obter_dados_caminho,
    obter_tamanho_arquivo,
    obter_data_criacao,
    obter_data_modificacao,
    obter_data_acesso,
    obter_permissoes_caminho,
    obter_id_unico,
)

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)


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
        if not caminho_original.strip():
            raise ValueError(
                "O caminho não pode ser vazio ou composto apenas por espaços."
            )

        caracteres_invalidos = ["?", "*", "|", "<", ">"]
        if any(char in caminho_original for char in caracteres_invalidos):
            raise ValueError(
                f"O caminho contém caracteres inválidos: {caracteres_invalidos}"
            )

        self.caminho_original = caminho_original
        self.caminho_resolvido = self._converter_para_absoluto(self.caminho_original)
        self.existe = self._verificar_existencia()
        self.is_arquivo = self._verificar_se_e_arquivo()
        self.is_diretorio = self._verificar_se_e_diretorio()
        self.dados_filtrados = obter_dados_caminho(self.caminho_resolvido)

    def _verificar_existencia(self) -> bool:
        """
        Verifica se o caminho existe no sistema de arquivos.

        Returns:
            bool: True se o caminho existir, False caso contrário.
        """
        try:
            return Path(self.caminho_resolvido).exists()
        except OSError as erro:
            logging.error(
                "Erro ao verificar a existência do caminho '%s': %s",
                self.caminho_resolvido,
                erro,
            )
            return False

    def _verificar_se_e_arquivo(self) -> bool:
        """
        Verifica se o caminho é um arquivo.

        Returns:
            bool: True se o caminho for um arquivo, False caso contrário.
        """
        try:
            return Path(self.caminho_resolvido).is_file()
        except OSError as erro:
            logging.error("Erro ao verificar se é arquivo: %s", erro)
            return False

    def _verificar_se_e_diretorio(self) -> bool:
        """
        Verifica se o caminho é um diretório.

        Returns:
            bool: True se o caminho for um diretório, False caso contrário.
        """
        try:
            return Path(self.caminho_resolvido).is_dir()
        except OSError as erro:
            logging.error("Erro ao verificar se é diretório: %s", erro)
            return False

    def _converter_para_absoluto(self, caminho_relativo: str) -> str:
        """
        Converte um caminho relativo para absoluto, utilizando a função de sanitização.

        Args:
            caminho_relativo (str): O caminho a ser processado.

        Returns:
            str: O caminho absoluto resolvido.
        """
        caminho_absoluto = str(
            Path(caminho_relativo).resolve()
            if Path(caminho_relativo).is_absolute()
            else Path.home() / caminho_relativo.strip("/")
        )
        return caminho_absoluto

    def gerar_dados_caminho(self) -> dict[str, Union[str, bool]]:
        """
        Gera um dicionário com informações detalhadas sobre o caminho.

        Returns:
            dict[str, Union[str, bool]]: Informações sobre o caminho, incluindo:
                - caminho_original: O caminho original fornecido.
                - caminho_resolvido: O caminho absoluto resolvido.
                - existe: Indica se o caminho existe no sistema de arquivos.
                - is_arquivo: Indica se o caminho é um arquivo.
                - is_diretorio: Indica se o caminho é um diretório.
        """
        return {
            "caminho_original": self.caminho_original,
            "caminho_resolvido": self.caminho_resolvido,
            "dados_filtrados": self.dados_filtrados,
            "existe": self.existe,
            "is_arquivo": self.is_arquivo,
            "is_diretorio": self.is_diretorio,
        }

    def para_json(self) -> str:
        """
        Converte o objeto PathModel em uma representação JSON.

        Returns:
            str: Representação JSON do objeto PathModel.
        """
        return json.dumps(
            self.gerar_dados_caminho(), indent=4, ensure_ascii=False, sort_keys=True
        )


# Exemplo de uso
if __name__ == "__main__":
    caminhos = [
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
        "/home/pedro-pm-dias/Downloads/Chrome/",
        "/home/pedro-pm-dias/Downloads/Chrome/Teste/",
        "/caminho/inexistente/",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "../../Downloads/Chrome/favoritos.html",
        "../../Downloads/Chrome/",
        "../../Downloads/Chrome/Teste/",
    ]

    for caminho in caminhos:
        path_obj: PathModel = PathModel(caminho)
        path_obj_dict: dict[str, Union[str, bool]] = path_obj.gerar_dados_caminho()
        print(path_obj_dict, end="\n\n")


class FileModel(PathModel):
    """
    Classe que representa e manipula um arquivo no sistema operacional.
    """

    def __init__(self, caminho_original: str):
        """
        Inicializa um objeto FileModel a partir de um caminho de arquivo.
        """
        super().__init__(caminho_original)

        if not self.existe:
            logging.warning("O arquivo '%s' não existe.", self.caminho_resolvido)

        if not self.is_arquivo:
            logging.warning(
                "O caminho '%s' não é um arquivo válido.", self.caminho_resolvido
            )

        self.dados_stat = self._obter_dados_stat() if self.is_arquivo else None

    def _obter_dados_stat(self) -> os.stat_result:
        """
        Obtém os dados do método .stat() para o arquivo.

        Returns:
            os.stat_result: Objeto contendo as informações detalhadas do arquivo.
        """
        try:
            return Path(self.caminho_resolvido).stat()
        except FileNotFoundError:
            logging.error("Arquivo não encontrado: '%s'", self.caminho_resolvido)
        except OSError as erro:
            logging.error(
                "Erro ao obter informações do arquivo '%s': %s",
                self.caminho_resolvido,
                erro,
            )
        return None

    def gerar_dados_arquivo(self) -> dict[str, Union[str, int, bool]]:
        """
        Gera um dicionário com informações detalhadas sobre o arquivo.

        Returns:
            dict[str, Union[str, int, bool]]: Dados sobre o arquivo.
        """
        dados_arquivo = {
            "caminho_original": self.caminho_original,
            "caminho_resolvido": self.caminho_resolvido,
            "caminho_filtrado": self.dados_filtrados,
            "caminho_existe": self.existe,
            "caminho_e_arquivo": self.is_arquivo,
            "caminho_e_diretorio": self.is_diretorio,
        }

        if self.dados_stat:
            dados_arquivo.update(
                {
                    "tamanho_arquivo": obter_tamanho_arquivo(self.dados_stat.st_size),
                    "ultima_modificacao": obter_data_modificacao(
                        self.dados_stat.st_mtime
                    ),
                    "data_criacao": obter_data_criacao(self.dados_stat.st_ctime),
                    "ultimo_acesso": obter_data_acesso(self.dados_stat.st_atime),
                    "permissoes": obter_permissoes_caminho(
                        self.dados_stat.st_mode & 0o777
                    ),  # Permissões no estilo Unix
                    "proprietario_uid": obter_id_unico(self.dados_stat.st_uid),
                }
            )

        return dados_arquivo


# Exemplo de uso
if __name__ == "__main__":
    arquivos = [
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html",
        "../../Downloads/Chrome/favoritos_23_12_2024.html",
        "../../Downloads/Chrome/favoritos.html",
    ]

    for arquivo in arquivos:
        file_obj = FileModel(arquivo)
        file_obj_json = file_obj.gerar_dados_arquivo()
        print(file_obj_json, end="\n\n")
