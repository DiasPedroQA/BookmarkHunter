# main.py
# pylint: disable=C0114, C0115, C0116, E0401

"""Classe para verificar se o caminho é uma pasta."""


from controllers.path_check_controller import PathCheckController
from controllers.file_path_check_controller import FilePathCheckController
from controllers.folder_path_check_controller import FolderPathCheckController


def main():
    """Função principal."""
    path = "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html"

    # Exemplo de uso do PathCheckController
    path_check = PathCheckController(path)
    print(f"O caminho existe? {path_check.check_exists()}")

    # Exemplo de uso do FilePathCheckController
    file_check = FilePathCheckController(path)
    print(f"O caminho é um arquivo? {file_check.is_a_real_file()}")


    # Exemplo de uso do FolderPathCheckController
    folder_check = FolderPathCheckController(path)
    print(f"O caminho é uma pasta? {folder_check.is_a_real_folder()}")



# Executa a função principal
if __name__ == "__main__":
    main()
