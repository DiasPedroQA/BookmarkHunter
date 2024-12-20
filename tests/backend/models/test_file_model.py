# Criando os testes com testes com ferramenta alternativa

# import pytest
# from app.models import File, Folder
# from app.models.file_model import File
# from app.models.bookmark_model import Bookmark

# def test_file_initialization():
#     file = File("Example Folder")
#     assert file.name == "Example Folder"
#     assert file.folder is None
#     assert file.bookmarks == []

# def test_add_bookmark():
#     file = File("Example Folder")
#     bookmark = Bookmark("Example Title", "http://example.com")
#     file.add_bookmark(bookmark)
#     assert len(file.bookmarks) == 1
#     assert file.bookmarks[0] == bookmark
#     assert bookmark.file == file

# def test_add_multiple_bookmarks():
#     file = File("Example Folder")
#     bookmark1 = Bookmark("Title 1", "http://example1.com")
#     bookmark2 = Bookmark("Title 2", "http://example2.com")
#     file.add_bookmark(bookmark1)
#     file.add_bookmark(bookmark2)
#     assert len(file.bookmarks) == 2
#     assert bookmark1 in file.bookmarks
#     assert bookmark2 in file.bookmarks

# def test_file_repr():
#     file = File("Example Folder")
#     assert repr(file) == "<File(name=Example Folder)>"

# def test_file_with_folder():
#     file = File("Example Folder", folder="Example Folder Path")
#     assert file.folder == "Example Folder Path"


# Criando os testes com o CHATGPT

# def test_create_file():
#     # Criar uma pasta
#     folder = Folder(name="example_folder")

#     # Criar um arquivo associado à pasta
#     file = File(name="example_file")
#     folder.add_file(file)

#     # Verificar o arquivo
#     assert file.name == "example_file"
#     assert file.folder == folder
#     assert file in folder.files
