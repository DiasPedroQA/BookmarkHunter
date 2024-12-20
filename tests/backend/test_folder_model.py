# Criando os testes com testes com ferramenta alternativa

# import pytest
# from app.models import Folder
# from app.models.folder_model import Folder

# def test_folder_initialization():
#     folder = Folder("Documents")
#     assert folder.name == "Documents"
#     assert folder.files == []

# def test_add_file():
#     folder = Folder("Documents")
#     file = "file1.txt"
#     folder.add_file(file)
#     assert file in folder.files
#     assert folder.files[0] == file

# def test_add_multiple_files():
#     folder = Folder("Documents")
#     file1 = "file1.txt"
#     file2 = "file2.txt"
#     folder.add_file(file1)
#     folder.add_file(file2)
#     assert len(folder.files) == 2
#     assert file1 in folder.files
#     assert file2 in folder.files

# def test_file_folder_relationship():
#     folder = Folder("Documents")
#     file = "file1.txt"
#     folder.add_file(file)
#     assert hasattr(file, 'folder')
#     assert file.folder == folder

# def test_folder_repr():
#     folder = Folder("Documents")
#     assert repr(folder) == "<Folder(name=Documents)>"


# Criando os testes com o CHATGPT

# def test_create_folder():
#     # Criar uma pasta
#     folder = Folder(name="example_folder")

#     # Verificar a pasta
#     assert folder.name == "example_folder"
#     assert folder.files == []
