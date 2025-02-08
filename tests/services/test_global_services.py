# tests/services/test_global_services.py
# pylint: disable=C, R, E, W

import pytest
from pathlib import Path
from app.services.global_services import GeneralServices

caminho_verdadeiro: str = (
    "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html"
)


# Testes para o método __init__
def test_init_com_caminho_valido():
    caminho_valido: str = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_23_12_2024.html"
    )
    servico = GeneralServices(caminho_inicial=caminho_valido)
    assert servico.caminho == Path(caminho_valido)
    assert isinstance(servico.caminho, Path)
    assert servico.caminho_existe is True


def test_init_com_caminho_invalido():
    caminho_invalido: str = (
        "/home/pedro-pm-dias/Downloads/Chrome/favoritos_24_12_2024.html"
    )
    servico = GeneralServices(caminho_inicial=caminho_invalido)
    assert servico.caminho == Path(caminho_invalido)
    assert isinstance(servico.caminho, Path)
    assert servico.caminho_existe is False


def test_init_com_caminho_inexistente():
    servico = GeneralServices(caminho_inicial="/caminho/inexistente")
    assert servico.caminho_existe is False


# Testes para o método _formatar_timestamp
def test_formatar_timestamp():
    timestamp = 1672531199  # 31/12/2022 20:59:59
    resultado = GeneralServices._formatar_timestamp(timestamp)
    assert resultado == "31/12/2022 20:59:59"


# Testes para o método _converter_tamanho
def test_converter_tamanho_auto():
    resultado = GeneralServices._converter_tamanho(1500)
    assert resultado == "1.46 KB"


def test_converter_tamanho_em_mb():
    servico = GeneralServices(caminho_inicial="/caminho/qualquer")
    resultado = servico._converter_tamanho(1500000, "MB")
    assert resultado == "1.43 MB"


def test_converter_tamanho_unidade_invalida():
    with pytest.raises(
        ValueError, match="Unidade inválida. Use uma das seguintes:"
    ):
        GeneralServices._converter_tamanho(1500, "INVALIDO")


# Testes para o método _estatisticas_caminho
def test_estatisticas_caminho_valido():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    estatisticas = servico._estatisticas_caminho()
    assert estatisticas.st_size == 43973  # Tamanho do arquivo de teste


def test_estatisticas_caminho_invalido():
    servico = GeneralServices(caminho_inicial="/caminho/inexistente")
    with pytest.raises(FileNotFoundError, match="O arquivo ou diretório não existe."):
        servico._estatisticas_caminho()


# Testes para o método obter_tamanho_formatado
def test_obter_tamanho_formatado():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    assert servico.obter_tamanho_formatado() == "42.94 KB"


# Testes para o método obter_ultimo_acesso
def test_obter_ultimo_acesso():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    resultado = servico.obter_ultimo_acesso()
    assert isinstance(resultado, str)
    assert len(resultado) == 19  # Formato "dd/mm/aaaa HH:MM:SS"


# Testes para o método obter_ultima_modificacao
def test_obter_ultima_modificacao():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    resultado = servico.obter_ultima_modificacao()
    assert isinstance(resultado, str)
    assert len(resultado) == 19  # Formato "dd/mm/aaaa HH:MM:SS"


# Testes para o método obter_data_criacao
def test_obter_data_criacao():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    resultado = servico.obter_data_criacao()
    assert isinstance(resultado, str)
    assert len(resultado) == 19  # Formato "dd/mm/aaaa HH:MM:SS"


# Testes para o método obter_permissoes
def test_obter_permissoes():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    permissoes = servico.obter_permissoes()
    assert permissoes.startswith("0o")  # Permissões no formato octal


# Testes para o método obter_sistema_operacional
def test_obter_sistema_operacional():
    servico = GeneralServices(caminho_inicial="/caminho/qualquer")
    sistema = servico.obter_sistema_operacional()
    assert sistema in ["Windows", "Linux", "Darwin"]  # Sistemas operacionais comuns


# Testes para o método obter_metadados
def test_obter_metadados_arquivo():
    servico = GeneralServices(caminho_inicial=caminho_verdadeiro)
    metadados = servico.obter_metadados()
    assert "tamanho_formatado" in metadados
    assert "ultimo_acesso" in metadados
    assert "ultima_modificacao" in metadados
    assert "data_criacao" in metadados
    assert "permissoes" in metadados
    assert "sistema_operacional" in metadados

    # def test_obter_metadados_caminho_invalido():
    with pytest.raises(OSError, match="O arquivo ou diretório não existe."):
        GeneralServices(caminho_inicial="/home/../caminho/inexistente")
        # metadados = servico.obter_metadados()


# def test_obter_metadados_permissao_negada(monkeypatch: pytest.MonkeyPatch):
#     def mock_stat():
#         raise PermissionError("Permissão negada")

#     monkeypatch.setattr(Path, "stat", mock_stat)
#     servico = GeneralServices(caminho_inicial="/caminho/protegido")
#     metadados = servico.obter_metadados()
#     assert metadados == {
#         "erro": "Permissão negada para acessar o arquivo ou diretório."
#     }


# def test_obter_metadados_erro_os(monkeypatch: pytest.MonkeyPatch):
#     def mock_exists():
#         return True  # Simula que o caminho existe para evitar falha na inicialização

#     def mock_stat():
#         raise OSError("Erro genérico")

#     # Mocka o método exists para evitar falha na inicialização
#     monkeypatch.setattr(Path, "exists", mock_exists)
#     # Mocka o método stat para simular o erro
#     monkeypatch.setattr(Path, "stat", mock_stat)

#     servico = GeneralServices(caminho_inicial="/caminho/invalido")
#     metadados = servico.obter_metadados()
#     assert metadados == {"erro": "Erro ao obter metadados: Erro genérico"}
