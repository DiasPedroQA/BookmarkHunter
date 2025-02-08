# pylint: disable=C0114, C0115, C0116, E0401

"""
Controller para verificar se o caminho fornecido é um arquivo válido.
"""

from models.file_path_check import FilePathCheck


class FilePathCheckController:
    """
    Controller para verificar e validar arquivos.
    """

    def __init__(self, path):
        """
        Inicializa a classe com o caminho e realiza a verificação inicial.
        """
        self.file_path_check = FilePathCheck(path)

        # Verifica a existência do caminho já na inicialização
        if not self.file_path_check.path.exists():
            raise FileNotFoundError(f"O caminho '{path}' não existe.")

    def is_a_real_file(self):
        """
        Verifica se o caminho é um arquivo real
        e atende aos critérios de validação.
        """
        return self.file_path_check.is_a_real_file()

    def is_readable(self):
        """
        Verifica se o arquivo pode ser lido.
        """
        return self.file_path_check.is_readable()

    def is_writable(self):
        """
        Verifica se o arquivo pode ser escrito.
        """
        return self.file_path_check.is_writable()

    def has_valid_extension(self, allowed_extensions=None):
        """
        Verifica se o arquivo possui uma extensão permitida.
        """
        return self.file_path_check.has_valid_extension(allowed_extensions)

    def is_not_empty(self):
        """
        Verifica se o arquivo não está vazio (tamanho maior que 0).
        """
        return self.file_path_check.is_not_empty()

    def validate_file(self):
        """
        Método para validar o arquivo completo e lançar exceções se necessário.
        """
        if not self.is_a_real_file():
            raise ValueError(
                "O arquivo não é válido conforme os critérios estabelecidos."
            )
        return True
