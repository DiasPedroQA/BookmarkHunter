# pylint: disable=C0114, C0115, C0116, E0401

"""Controller para verificar caminhos de pastas."""

from models.folder_path_check import FolderPathCheck


class FolderPathCheckController:
    """Controller para verificar se um caminho é uma pasta válida."""

    def __init__(self, path):
        """Inicializa a classe com o caminho."""
        self.folder_path_check = FolderPathCheck(path)

    def validate_folder(self):
        """Valida a pasta com base nos critérios definidos na FolderPathCheck."""
        if not self.folder_path_check.is_a_real_folder():
            raise ValueError(f"A pasta '{self.folder_path_check.path}' não é válida.")
        return True

    def is_a_real_folder(self):
        """Verifica se o caminho é uma pasta válida."""
        return self.folder_path_check.is_a_real_folder()

    def is_readable(self):
        """Verifica se a pasta pode ser lida."""
        return self.folder_path_check.is_readable()

    def is_writable(self):
        """Verifica se a pasta pode ser escrita."""
        return self.folder_path_check.is_writable()

    def is_empty(self):
        """Verifica se a pasta está vazia."""
        return self.folder_path_check.is_not_empty_folder()
