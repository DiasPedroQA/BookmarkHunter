"""
Este módulo contém testes para o modelo de caminho (PathModel) da aplicação.
Os testes verificam a funcionalidade do modelo para diferentes tipos de caminhos,
incluindo caminhos absolutos e relativos, válidos e inválidos, arquivos e diretórios.

Testes incluídos:
- teste_caminho_absoluto_valido: Testa um caminho absoluto válido.
- teste_caminho_absoluto_invalido: Testa um caminho absoluto inválido.
- teste_caminho_absoluto_pasta: Testa um caminho absoluto de pasta.
- teste_caminho_absoluto_pasta_teste: Testa um caminho absoluto de pasta de teste.
- teste_caminho_absoluto_inexistente: Testa um caminho absoluto inexistente.
- test_caminho_relativo_valido: Testa um caminho relativo válido.
- test_caminho_relativo_invalido: Testa um caminho relativo inválido.
- test_caminho_relativo_pasta: Testa um caminho relativo de pasta.
- test_caminho_relativo_pasta_teste: Testa um caminho relativo de pasta de teste.
- test_caminho_relativo_inexistente: Testa um caminho relativo inexistente.
- test_inicialization_path_model: Testa a inicialização do modelo PathModel.
- test_caminho_valido: Testa a classe PathModel com um caminho válido.

"""

# pylint: disable=E0611, W0105

from app.models.modelo_caminho import PathModel


def teste_caminho_absoluto_valido():
    """
    Testa um caminho absoluto válido.
    """
    test_caminho_absoluto_valido = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    )
    caminho_modelo = PathModel(test_caminho_absoluto_valido)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == test_caminho_absoluto_valido


def teste_caminho_absoluto_invalido():
    """
    Testa um caminho absoluto inválido.
    """
    test_caminho_absoluto_invalido = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos.html"
    )
    caminho_modelo = PathModel(test_caminho_absoluto_invalido)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == test_caminho_absoluto_invalido


def teste_caminho_absoluto_pasta():
    """
    Testa um caminho absoluto de pasta.
    """
    test_caminho_absoluto_pasta = "/home/pedro-pm-dias/Downloads/Chrome/"
    caminho_modelo = PathModel(test_caminho_absoluto_pasta)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == test_caminho_absoluto_pasta


def teste_caminho_absoluto_pasta_teste():
    """
    Testa um caminho absoluto de pasta de teste.
    """
    test_caminho_absoluto_pasta_teste = "/home/pedro-pm-dias/Downloads/Chrome/Teste/"
    caminho_modelo = PathModel(test_caminho_absoluto_pasta_teste)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == test_caminho_absoluto_pasta_teste


def teste_caminho_absoluto_inexistente():
    """
    Testa um caminho absoluto inexistente.
    """
    test_caminho_absoluto_inexistente = (
        "/home/pedro-pm-dias/Downloads/caminho/inexistente/"
    )
    caminho_modelo = PathModel(test_caminho_absoluto_inexistente)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == test_caminho_absoluto_inexistente


def test_caminho_relativo_valido():
    """
    Testa um caminho relativo válido.
    """
    teste_caminho_relativo_valido = "../../Downloads/Chrome/favoritos_23_12_2024.html"
    caminho_modelo = PathModel(teste_caminho_relativo_valido)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == teste_caminho_relativo_valido


def test_caminho_relativo_invalido():
    """
    Testa um caminho relativo inválido.
    """
    teste_caminho_relativo_invalido = "../../Downloads/Chrome/favoritos.html"
    caminho_modelo = PathModel(teste_caminho_relativo_invalido)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == teste_caminho_relativo_invalido


def test_caminho_relativo_pasta():
    """
    Testa um caminho relativo de pasta.
    """
    teste_caminho_relativo_pasta = "../../Downloads/Chrome/"
    caminho_modelo = PathModel(teste_caminho_relativo_pasta)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == teste_caminho_relativo_pasta


def test_caminho_relativo_pasta_teste():
    """
    Testa um caminho relativo de pasta de teste.
    """
    teste_caminho_relativo_pasta_teste = "../../Downloads/Chrome/Teste/"
    caminho_modelo = PathModel(teste_caminho_relativo_pasta_teste)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == teste_caminho_relativo_pasta_teste


def test_caminho_relativo_inexistente():
    """
    Testa um caminho relativo inexistente.
    """
    teste_caminho_relativo_inexistente = "../../Downloads/caminho/inexistente/"
    caminho_modelo = PathModel(teste_caminho_relativo_inexistente)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == teste_caminho_relativo_inexistente


def test_inicialization_path_model():
    """
    Testa a inicialização do modelo PathModel.
    """
    caminho_de_teste = "../../Downloads/Chrome/"
    caminho_modelo = PathModel(caminho_de_teste)
    dados_teste = caminho_modelo.gerar_dados()
    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == caminho_de_teste
    assert dados_teste["caminho_resolvido"] == "/home/pedro-pm-dias/Downloads/Chrome/"
    assert dados_teste["caminho_existe"] is True
    assert dados_teste["is_arquivo"] is False
    assert dados_teste["is_diretorio"] is True
    assert dados_teste["permissoes"]["leitura"] is True
    assert dados_teste["permissoes"]["escrita"] is True
    assert dados_teste["permissoes"]["execucao"] is True
    assert dados_teste["estatisticas"]["data_acesso"] == "11/01/2025 23:50:03"
    assert dados_teste["estatisticas"]["data_criacao"] == "30/12/2024 03:55:01"
    assert dados_teste["estatisticas"]["data_modificacao"] == "30/12/2024 03:55:01"
    assert dados_teste["estatisticas"]["tamanho"] == "4.00 KB"
    assert dados_teste["dados_filtrados"]["pasta_pai"] == "home/pedro-pm-dias/Downloads"
    assert dados_teste["dados_filtrados"]["nome_pasta"] == "Chrome"


def test_caminho_valido():
    """
    Testa a classe PathModel com um caminho válido.
    """
    caminho_arquivo_valido = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    )
    caminho_modelo = PathModel(caminho_arquivo_valido)
    dados_teste = caminho_modelo.gerar_dados()

    # assert len(dados_teste["id_caminho"]) > 1
    assert dados_teste["caminho_original"] == caminho_arquivo_valido
    assert dados_teste["caminho_resolvido"] == caminho_arquivo_valido
    assert dados_teste["caminho_existe"] is True
    assert dados_teste["is_arquivo"] is True
    assert dados_teste["is_diretorio"] is False
    assert dados_teste["permissoes"]["leitura"] is True
    assert dados_teste["permissoes"]["escrita"] is True
    assert dados_teste["permissoes"]["execucao"] is False
    assert dados_teste["estatisticas"]["data_acesso"] == "10/01/2025 22:36:35"
    assert dados_teste["estatisticas"]["data_criacao"] == "24/12/2024 18:07:20"
    assert dados_teste["estatisticas"]["data_modificacao"] == "24/12/2024 18:07:20"
    assert dados_teste["estatisticas"]["tamanho"] == "1010.17 KB"
    assert (
        dados_teste["dados_filtrados"]["pasta_pai"]
        == "home/pedro-pm-dias/Downloads/Chrome"
    )
    assert dados_teste["dados_filtrados"]["nome_arquivo"] == "favoritos_23_12_2024"
    assert dados_teste["dados_filtrados"]["extensao_arquivo"] == "html"


"""

{
    "id_caminho": "18c2f394-3c7e-519c-9232-7a4470c7868f",
    "caminho_original": "../../Downloads/Chrome/favoritos_23_12_2024.html",
    "caminho_resolvido": "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html",
    "caminho_existe": True,
    "estatisticas": {
        "data_acesso": "10/01/2025 22:36:35",
        "data_criacao": "24/12/2024 18:07:20",
        "data_modificacao": "24/12/2024 18:07:20",
        "tamanho": "1010.17 KB",
    },
    "is_arquivo": True,
    "is_diretorio": False,
    "permissoes": {"leitura": True, "escrita": True, "execucao": False},
    "dados_filtrados": {
        "pasta_pai": "home/pedro-pm-dias/Downloads/Chrome",
        "nome_arquivo": "favoritos_23_12_2024",
        "extensao_arquivo": "html",
    },
}


{
    "id_caminho": "facb7618-55ca-5c30-9cba-fd567b6c0611",
    "caminho_original": "../../Downloads/Chrome/",
    "caminho_resolvido": "/home/pedro-pm-dias/Downloads/Chrome/",
    "caminho_existe": True,
    "estatisticas": {
        "data_acesso": "10/01/2025 22:36:35",
        "data_criacao": "24/12/2024 18:07:20",
        "data_modificacao": "24/12/2024 18:07:20",
        "tamanho": "4.00 KB",
    },
    "is_arquivo": False,
    "is_diretorio": True,
    "permissoes": {"leitura": True, "escrita": True, "execucao": True},
    "dados_filtrados": {
        "pasta_pai": "home/pedro-pm-dias/Downloads",
        "nome_pasta": "Chrome",
    },
}

"""
