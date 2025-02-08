# pylint: disable=C0114, C0115, C0116, E0401

"""
Classe para verificar se o caminho é um arquivo válido.
"""

from models.path_check import PathCheck


class FilePathCheck(PathCheck):
    """
    Classe para verificar se o caminho é um arquivo válido.
    """

    def is_a_real_file(self):
        """
        Verifica se o caminho é um arquivo real
        e atende a critérios de validação.
        """
        return (
            self.path.exists()  # Verifica se o caminho existe
            and self.path.is_file()  # Verifica se é um arquivo
            and not self.path.is_symlink()  # Evita links simbólicos
            and self.is_readable()  # Verifica se é legível
            and self.is_writable()  # Verifica se é gravável
            and self.has_valid_extension()  # Verifica a extensão do arquivo
            and self.is_not_empty()  # Verifica se o arquivo não está vazio
        )

    def has_valid_extension(self, allowed_extensions=None):
        """
        Verifica se o arquivo possui uma extensão permitida.
        """
        if allowed_extensions is None:
            allowed_extensions = {".html", ".htm"}
        if not allowed_extensions:
            raise ValueError("Nenhuma extensão permitida definida.")
        return self.path.suffix.lower() in allowed_extensions

    def is_not_empty(self):
        """
        Verifica se o arquivo não está vazio (tamanho maior que 0).
        """
        return self.path.stat().st_size > 0

    def get_file_size(self):
        """
        Retorna o tamanho do arquivo em bytes.
        """
        return self.path.stat().st_size if self.path.is_file() else 0
