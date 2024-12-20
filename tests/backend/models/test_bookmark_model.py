# Criando os testes com testes com ferramenta alternativa

# import pytest
# from app.models import Bookmark, File
# from app.models.bookmark_model import Bookmark


# def test_bookmark_initialization():
#     bookmark = Bookmark("Example Title", "http://example.com")
#     assert bookmark.title == "Example Title"
#     assert bookmark.url == "http://example.com"
#     assert bookmark.file is None

# def test_bookmark_with_file():
#     bookmark = Bookmark("Example Title", "http://example.com", file="example_file.txt")
#     assert bookmark.file == "example_file.txt"

# def test_bookmark_repr():
#     bookmark = Bookmark("Example Title", "http://example.com")
#     assert repr(bookmark) == "<Bookmark(title=Example Title, url=http://example.com)>"

# def test_bookmark_title_change():
#     bookmark = Bookmark("Old Title", "http://example.com")
#     bookmark.title = "New Title"
#     assert bookmark.title == "New Title"

# def test_bookmark_url_change():
#     bookmark = Bookmark("Example Title", "http://old-url.com")
#     bookmark.url = "http://new-url.com"
#     assert bookmark.url == "http://new-url.com"


# Criando os testes com o CHATGPT

# def test_create_bookmark():
#     # Criar um arquivo
#     file = File(name="example_file")

#     # Criar um bookmark associado ao arquivo
#     bookmark = Bookmark(title="Example Bookmark", url="https://example.com")
#     file.add_bookmark(bookmark)

#     # Verificar o bookmark
#     assert bookmark.title == "Example Bookmark"
#     assert bookmark.url == "https://example.com"
#     assert bookmark.file == file
#     assert bookmark in file.bookmarks

# def test_bookmark_initialization_with_no_file():
#     bookmark = Bookmark("No File Title", "http://no-file.com")
#     assert bookmark.file is None

# def test_bookmark_repr_with_file():
#     file = "example_file.txt"
#     bookmark = Bookmark("File Title", "http://file-url.com", file=file)
#     assert repr(bookmark) == "<Bookmark(title=File Title, url=http://file-url.com)>"

# def test_bookmark_title_empty_string():
#     bookmark = Bookmark("", "http://empty-title.com")
#     assert bookmark.title == ""

# def test_bookmark_url_invalid_format():
#     bookmark = Bookmark("Invalid URL", "invalid-url")
#     assert bookmark.url == "invalid-url"

# def test_bookmark_title_length_exceeding_limit():
#     long_title = "A" * 256
#     bookmark = Bookmark(long_title, "http://long-title.com")
#     assert bookmark.title == long_title
