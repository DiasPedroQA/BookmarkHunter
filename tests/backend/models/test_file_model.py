# tests/backend/models/test_file_model.py

"""
Testes para o modelo do objeto Arquivo.
"""

import os
import sys
from pathlib import Path


# Adiciona o diretório raiz ao PYTHONPATH para permitir importações absolutas  # pylint: disable=C0413
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from app.models.file_model import ObjetoArquivo
# from app.models.bookmark_model import ObjetoTag


# def test_file_initialization():
#     """
#     Testa a inicialização de um objeto arquivo, garantindo que o nome
#     seja atribuído corretamente, o diretório da pasta seja None e os
#     bookmarks sejam uma lista vazia.
#     """
#     file = ObjetoArquivo("Exemplo de Pasta")
#     assert file.name == "Exemplo de Pasta"
#     assert file.folder is None
#     assert file.bookmarks == []


# def test_add_bookmark():
#     """
#     Testa o método de adicionar um bookmark a um arquivo, verificando
#     se o bookmark foi adicionado corretamente e se o relacionamento
#     entre o arquivo e o bookmark foi estabelecido.
#     """
#     file = ObjetoArquivo("Exemplo de Pasta")
#     bookmark = ObjetoTag("Exemplo de Título", "http://exemplo.com")
#     file.add_bookmark(bookmark)
#     assert len(file.bookmarks) == 1
#     assert file.bookmarks[0] == bookmark
#     assert bookmark.file == file


# def test_add_multiple_bookmarks():
#     """
#     Testa a adição de múltiplos bookmarks a um arquivo, garantindo que
#     os bookmarks sejam adicionados corretamente à lista de bookmarks.
#     """
#     file = ObjetoArquivo("Exemplo de Pasta")
#     bookmark1 = ObjetoTag("Título 1", "http://exemplo1.com")
#     bookmark2 = ObjetoTag("Título 2", "http://exemplo2.com")
#     file.add_bookmark(bookmark1)
#     file.add_bookmark(bookmark2)
#     assert len(file.bookmarks) == 2
#     assert bookmark1 in file.bookmarks
#     assert bookmark2 in file.bookmarks


def test_file_repr():
    """
    Testa a representação de string (repr) de um arquivo, verificando
    se a representação está correta.
    """
    file = ObjetoArquivo("Exemplo de Pasta")
    assert repr(file) == "<ObjetoArquivo(name=Exemplo de Pasta)>"


# def test_file_with_folder():
#     """
#     Testa a criação de um arquivo associado a uma pasta, garantindo
#     que o arquivo tenha a pasta correta associada.
#     """
#     file = ObjetoArquivo(caminho="Caminho/para/Pasta")
#     assert file.folder == "Caminho/para/Pasta"


# def test_create_file():
#     """
#     Testa a criação de um arquivo dentro de uma pasta, verificando se
#     o arquivo foi corretamente associado à pasta.
#     """
#     folder = Folder(name="pasta_exemplo")
#     file = ObjetoArquivo(caminho="arquivo_exemplo")
#     folder.add_file(file)
#     assert file.name == "arquivo_exemplo"
#     assert file.folder == folder
#     assert file in folder.files


# def test_file_absolute_path():
#     """
#     Testa o método de verificação de caminho absoluto de um arquivo,
#     garantindo que o método identifique corretamente os caminhos absolutos.
#     """
#     file = ObjetoArquivo("/home/usuario/Downloads/Chrome/favoritos_23_12_2024.html")
#     assert file._eh_caminho_absoluto() is True


# def test_file_not_found():
#     """
#     Testa a verificação de um arquivo inexistente, garantindo que
#     o método retorne um dicionário vazio quando o arquivo não for encontrado.
#     """
#     file = ObjetoArquivo("/caminho/invalido/para/arquivo.txt")
#     assert file.obter_informacoes_arquivo() == {}


# def test_file_size_conversion():
#     """
#     Testa a conversão de tamanho de arquivo, garantindo que o método
#     de obtenção de tamanho funcione corretamente.
#     """
#     file = ObjetoArquivo("/home/usuario/Downloads/Chrome/favoritos_23_12_2024.html")
#     size = file._obter_tamanho_arquivo()
#     assert size is not None


def test_get_parent_directory():
    """
    Testa a obtenção do diretório pai de um arquivo, garantindo que
    o método retorne corretamente o diretório pai do arquivo.
    """
    file = ObjetoArquivo("/home/usuario/Downloads/Chrome/favoritos_23_12_2024.html")
    parent_dir = file.obter_diretorio_pai()
    assert parent_dir == Path("/home/usuario/Downloads/Chrome")


def test_file_existence_check():
    """
    Testa a verificação de existência de um arquivo, garantindo que
    o método retorne True quando o arquivo existir.
    """
    file = ObjetoArquivo("/home/usuario/Downloads/Chrome/favoritos_23_12_2024.html")
    assert file.verificar_existencia_arquivo() is True


def test_read_non_existent_file():
    """
    Testa a leitura de um arquivo inexistente, garantindo que o método
    retorne None quando o arquivo não for encontrado.
    """
    file = ObjetoArquivo("/caminho/invalido/para/arquivo.txt")
    assert file.ler_arquivo() is None


def test_create_file_with_content():
    """
    Testa a criação de um arquivo com conteúdo, verificando se o
    conteúdo pode ser lido corretamente após a criação.
    """
    file = ObjetoArquivo("/home/usuario/Downloads/Chrome/arquivo_teste.txt")
    assert file.criar_novo_arquivo("Conteúdo de teste") is True
    assert file.ler_arquivo() == "Conteúdo de teste"


# def test_rename_file():
#     """
#     Testa a funcionalidade de renomear um arquivo, verificando se o
#     nome do arquivo é alterado corretamente após a operação de renomeação.
#     """
#     file = ObjetoArquivo("/home/usuario/Downloads/Chrome/arquivo_teste.txt")
#     file.criar_novo_arquivo("Conteúdo de teste")
#     new_path = file._ObjetoArquivo__renomear_arquivo("_renomeado", ".txt")
#     assert new_path.name == "arquivo_teste_renomeado.txt"


# def test_move_file():
#     """
#     Testa a funcionalidade de mover um arquivo para uma nova pasta,
#     garantindo que o arquivo seja movido corretamente para o novo local.
#     """
#     file = ObjetoArquivo("/home/usuario/Downloads/Chrome/arquivo_teste.txt")
#     file.criar_novo_arquivo("Conteúdo de teste")
#     new_path = file._ObjetoArquivo__mover_arquivo("/home/usuario/Downloads/Chrome/NovaPasta")
#     assert new_path.name == "arquivo_teste.txt"
