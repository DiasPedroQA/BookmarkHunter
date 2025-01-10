from app.utils.ajuste_caminhos import ajustar_caminho_importacao

# Ajusta os caminhos de importação, se necessário
ajustar_caminho_importacao()

from app.utils.conversores import (
    validar_caminho,
    analisar_profundidade,
    verificar_extensao,
    limpar_caminho,
)

def test_validar_caminho():
    assert validar_caminho("/home/user/valid/path")
    assert not validar_caminho("/home/user/invalid/path//")
    assert not validar_caminho("/home/user/invalid/path/<>")
    assert not validar_caminho("")

def test_analisar_profundidade():
    assert analisar_profundidade("/home/user/valid/path") == (('/home', '/user', '/valid', '/path'), 4)
    assert analisar_profundidade("/home/user/") == (('/home', '/user'), 2)
    assert analisar_profundidade("/") == ((), 0)

def test_verificar_extensao():
    assert verificar_extensao("/home/user/file.txt", ["txt", "md"])
    assert not verificar_extensao("/home/user/file.txt", ["md", "html"])
    assert verificar_extensao("/home/user/file.html", ["html"])
    assert not verificar_extensao("/home/user/file", ["html"])

def test_limpar_caminho():
    assert limpar_caminho("/home/user/valid/path/") == "home/user/valid/path"
    assert limpar_caminho("/home/user/valid/path") == "home/user/valid/path"
    assert limpar_caminho("home/user/valid/path/") == "home/user/valid/path"
    assert limpar_caminho("home/user/valid/path") == "home/user/valid/path"
