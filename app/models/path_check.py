# pylint: disable=C0114, C0115, C0116, E0401

"""
Classe base para verificar caminhos.
"""

from pathlib import Path


class PathCheck:
    """
    Classe base para verificar caminhos.
    """

    def __init__(self, path):
        """
        Inicializa a classe com o caminho.
        """
        self.path = Path(path)

    def path_exists(self):
        """
        Verifica se o caminho existe.
        """
        return self.path.exists()

    def is_not_symlink(self):
        """
        Verifica se o caminho não é um link simbólico.
        """
        return not self.path.is_symlink()

    def get_absolute_path(self):
        """
        Retorna o caminho absoluto.
        """
        return self.path.resolve()

    def get_metadata(self):
        """
        Obtém as informações do arquivo/pasta se existir.
        """
        return self.path.stat() if self.path_exists() else None

    def is_readable(self):
        """
        Verifica se o caminho pode ser lido.
        """
        stats = self.get_metadata()
        return stats and stats.st_mode & 0o444  # Permissões de leitura

    def is_writable(self):
        """
        Verifica se o caminho pode ser escrito.
        """
        stats = self.get_metadata()
        return stats and stats.st_mode & 0o222  # Permissões de escrita

    def get_creation_time(self):
        """
        Obtém a data de criação do caminho.
        """
        stats = self.get_metadata()
        return stats.st_ctime if stats else None

    def get_modification_time(self):
        """
        Obtém a última data de modificação do caminho.
        """
        stats = self.get_metadata()
        return stats.st_mtime if stats else None

    def get_access_time(self):
        """
        Obtém a última data de acesso ao caminho.
        """
        stats = self.get_metadata()
        return stats.st_atime if stats else None
