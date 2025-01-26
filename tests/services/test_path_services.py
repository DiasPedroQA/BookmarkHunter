# pylint: disable=C, R, E, W

# Importações

from app.services.path_services import extrair_nome_item, extrair_pasta_mae, obter_permissoes_caminho


def test_extrair_pasta_mae():
    assert extrair_pasta_mae("/home/pedro-pm-dias/Downloads/Chrome/file.txt") == "Chrome"
    assert extrair_pasta_mae("/home/pedro-pm-dias/Downloads/") == "Downloads"
    assert extrair_pasta_mae("/home/pedro-pm-dias/") == "pedro-pm-dias"
    assert extrair_pasta_mae("/home/") == "home"
    assert extrair_pasta_mae("/") is None
    assert extrair_pasta_mae("") is None


def test_obter_permissoes_caminho():
    permissoes = obter_permissoes_caminho("/home/user/docs")
    assert permissoes == "O caminho '/home/user/docs' não existe."
    permissoes = obter_permissoes_caminho("/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html")
    assert permissoes == {"leitura": True, "escrita": True, "execucao": False}
    permissoes = obter_permissoes_caminho("/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html")
    assert permissoes == {"leitura": True, "escrita": True, "execucao": False}
    permissoes = obter_permissoes_caminho("/home/user/docs/file.txt")
    assert permissoes == "O caminho '/home/user/docs/file.txt' não existe."


def test_extrair_nome_item():
    assert extrair_nome_item("/home/pedro-pm-dias/Downloads/Chrome/file.txt") == "file.txt"
    assert extrair_nome_item("/home/pedro-pm-dias/Downloads/Chrome") == "Chrome"
    assert extrair_nome_item("/home/user/") == "user"
    assert extrair_nome_item("/home") == "home"
    assert extrair_nome_item("/") == ""
    assert extrair_nome_item("") is None
