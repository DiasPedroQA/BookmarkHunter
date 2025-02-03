# pylint: disable=C0114, C0115, C0116, E0401

"""Classe para verificar caminhos de pastas."""

from models.path_check import PathCheck


class FolderPathCheck(PathCheck):
    """Classe para verificar caminhos de pastas."""

    def is_a_real_folder(self):
        """Verifica se o caminho é uma pasta real e válida."""
        return (
            self.path.exists()  # Verifica apenas uma vez a existência
            and self.path.is_dir()  # Verifica se é um diretório
            and not self.path.is_file()  # Evita arquivos
            and not self.path.is_symlink()  # Evita links simbólicos
            and self.is_readable()  # Verifica se pode ser lido
            and self.is_writable()  # Verifica se pode ser escrito
            and self.is_not_empty_folder()  # Verifica se a pasta não está vazia
        )

    def is_not_empty_folder(self):
        """Verifica se a pasta está vazia."""
        return any(self.path.iterdir())  # Verifica se existe algum item na pasta

    def list_files(self):
        """Retorna uma lista de arquivos dentro da pasta."""
        return [file for file in self.path.iterdir() if file.is_file()]

    def get_folder_size(self):
        """Retorna o tamanho total da pasta somando os arquivos dentro."""
        return sum(
            file.stat().st_size for file in self.path.iterdir() if file.is_file()
        )
