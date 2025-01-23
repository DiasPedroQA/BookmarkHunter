# pylint: disable=C, R, E, W

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.models.analisador_pathlib import PathlibCaminho


@pytest.fixture
def mock_sanitize_path():
    with patch("analisador_pathlib.SanitizePath") as mock_class:
        instance = mock_class.return_value
        instance.formato_valido = True
        instance.gerar_json.return_value = json.dumps(
            {"caminho_original": "/mock/path", "formato_valido": True}
        )
        yield instance


def test_pathlib_caminho_init():
    caminho = PathlibCaminho(caminho_original="/mock/path")
    assert caminho.caminho_original == "/mock/path"
    assert not caminho.caminho_existe
    assert caminho.tamanho_em_bytes == 0
    assert caminho.data_criacao == 0.0
    assert caminho.data_modificacao == 0.0
    assert caminho.data_acesso == 0.0


def test_pathlib_caminho_invalid_init():
    with pytest.raises(ValueError):
        PathlibCaminho(caminho_original="")


def test_verificar_se_caminho_existe():
    caminho = PathlibCaminho(caminho_original="/mock/path")
    with patch.object(Path, "exists", return_value=True):
        caminho.verificar_se_caminho_existe()
        assert caminho.caminho_existe


def test_definir_metadados():
    caminho = PathlibCaminho(caminho_original="/mock/path")
    mock_stat = MagicMock()
    mock_stat.st_size = 1024
    mock_stat.st_ctime = 1609459200.0
    mock_stat.st_mtime = 1609459200.0
    mock_stat.st_atime = 1609459200.0
    with patch.object(Path, "exists", return_value=True):
        with patch.object(Path, "stat", return_value=mock_stat):
            caminho.definir_metadados()
            assert caminho.tamanho_em_bytes == 1024
            assert caminho.data_criacao == 1609459200.0
            assert caminho.data_modificacao == 1609459200.0
            assert caminho.data_acesso == 1609459200.0


def test_definir_permissoes():
    caminho = PathlibCaminho(caminho_original="/mock/path")
    with patch("os.access", side_effect=[True, False, True]):
        caminho.definir_permissoes()
        assert caminho.permissao_leitura
        assert not caminho.permissao_escrita
        assert caminho.permissao_execucao


def test_obter_informacoes():
    caminho = PathlibCaminho(caminho_original="/mock/path")
    with patch.object(PathlibCaminho, "verificar_se_caminho_existe") as mock_verificar:
        with patch.object(PathlibCaminho, "definir_metadados") as mock_metadados:
            with patch.object(PathlibCaminho, "definir_permissoes") as mock_permissoes:
                info = caminho.obter_informacoes()
                assert info["caminho_original"] == "/mock/path"
                mock_verificar.assert_called_once()
                mock_metadados.assert_called_once()
                mock_permissoes.assert_called_once()
