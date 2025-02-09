# pylint: disable=C0114, C0115, C0116, E0401

"""
Controller para verificar a validade de um caminho e suas propriedades.
"""


from app.models.path_check import PathCheck


class PathCheckController:
    """
    Classe para verificar a validade de um caminho e suas propriedades.
    """

    def __init__(self, path):
        """
        Inicializa a classe com o caminho.
        """
        self.path_check = PathCheck(path)

    def check_exists(self):
        """
        Verifica se o caminho existe.
        """
        return self.path_check.path_exists()

    def is_readable_and_writable(self):
        """
        Verifica se o caminho pode ser lido e pode ser escrito.
        """
        return self.path_check.is_readable() and self.path_check.is_writable()

    def is_not_symlink(self):
        """
        Verifica se o caminho não é um link simbólico.
        """
        return self.path_check.is_not_symlink()

    def get_absolute_path(self):
        """
        Retorna o caminho absoluto.
        """
        return self.path_check.get_absolute_path()

    def get_path_timing(self):
        """
        Obtém as datas de último acesso, última modificação e criação do caminho.
        """
        return {
            "path_creation_time": self.path_check.get_creation_time(),
            "path_modification_time": self.path_check.get_modification_time(),
            "path_access_time": self.path_check.get_access_time(),
        }

    def validate_path(self):
        """
        Valida se o caminho existe e é utilizável (leitura e escrita).
        """
        if not self.check_exists():
            raise FileNotFoundError("Caminho não encontrado.")

        if not self.is_readable_and_writable():
            raise PermissionError("Permissões insuficientes para leitura e/ou escrita.")

        if not self.is_not_symlink():
            raise ValueError("O caminho não pode ser um link simbólico.")

        return True
