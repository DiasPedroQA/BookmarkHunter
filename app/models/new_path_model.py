# pylint: disable=C, R, E, W

import re

class PathAnalyzer:
    """
    Classe para analisar caminhos de arquivos e pastas no sistema operacional Ubuntu.
    Trabalha com strings e utiliza regex como auxiliar para validações.
    """

    def __init__(self, path):
        """
        Inicializa o analisador com um caminho fornecido.

        :param path: Caminho do arquivo ou pasta como string.
        """
        self.path = path

    def is_absolute(self):
        """
        Verifica se o caminho é absoluto com base em regras simples.

        :return: True se começar com '/', False caso contrário.
        """
        return self.path.startswith("/")

    def is_valid_path(self):
        """
        Verifica se o caminho contém apenas caracteres válidos.

        :return: True se o caminho for válido, False caso contrário.
        """
        pattern = r"^[\w\-./]+$"
        return bool(re.match(pattern, self.path))

    def get_basename(self):
        """
        Retorna o nome do arquivo ou pasta no final do caminho.

        :return: O nome do arquivo ou pasta.
        """
        parts = self.path.rstrip("/").split("/")
        return parts[-1] if parts else ""

    def get_directory(self):
        """
        Retorna o diretório pai do caminho fornecido.

        :return: O diretório pai.
        """
        if "/" not in self.path.rstrip("/"):
            return ""
        return "/".join(self.path.rstrip("/").split("/")[:-1])

    def has_extension(self, extension):
        """
        Verifica se o caminho possui uma extensão específica.

        :param extension: Extensão do arquivo (e.g., '.html').
        :return: True se o arquivo tiver a extensão, False caso contrário.
        """
        return self.path.endswith(extension)

    def count_segments(self):
        """
        Conta quantos segmentos existem no caminho.

        :return: Número de segmentos no caminho.
        """
        return len([segment for segment in self.path.strip("/").split("/") if segment])
