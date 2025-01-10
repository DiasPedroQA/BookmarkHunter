# pylint: disable=C, E0401, R0902, W

import json
import pytest
from pathlib import Path

from ajuste_caminhos import ajustar_caminho_importacao

# Ajusta os caminhos de importação, se necessário
ajustar_caminho_importacao()

from app.models.base_path_model import BasePathModel


@pytest.fixture
def setup_paths():
    return {
        "relative_file_path": "../../Downloads/Chrome/copy-favoritos_23_12_2024.html",
        "relative_dir_path": "../../Downloads/Chrome/",
        "absolute_file_path": "/home/pedro-pm-dias/Downloads/Chrome/copy-favoritos_23_12_2024.html",
        "absolute_dir_path": "/home/pedro-pm-dias/Downloads/Chrome/",
    }


def test_resolver_caminho_relative_file(setup_paths):
    model = BasePathModel(setup_paths["relative_file_path"])
    resolved_path = model._resolver_caminho(setup_paths["relative_file_path"])
    expected_path = Path.home() / "Downloads/Chrome/copy-favoritos_23_12_2024.html"
    assert resolved_path == expected_path.resolve()


def test_resolver_caminho_relative_dir(setup_paths):
    model = BasePathModel(setup_paths["relative_dir_path"])
    resolved_path = model._resolver_caminho(setup_paths["relative_dir_path"])
    expected_path = Path.home() / "Downloads/Chrome/"
    assert resolved_path == expected_path.resolve()


def test_resolver_caminho_absolute_file(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    resolved_path = model._resolver_caminho(setup_paths["absolute_file_path"])
    assert resolved_path == Path(setup_paths["absolute_file_path"]).resolve()


def test_resolver_caminho_absolute_dir(setup_paths):
    model = BasePathModel(setup_paths["absolute_dir_path"])
    resolved_path = model._resolver_caminho(setup_paths["absolute_dir_path"])
    assert resolved_path == Path(setup_paths["absolute_dir_path"]).resolve()


def test_caminho_existe(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    assert model.caminho_existe()


def test_tipo_caminho(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    assert model.tipo_caminho() == "absoluto"


def test_tipo_item(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    assert model.tipo_item() == "arquivo"


def test_get_nome_item(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    assert model.get_nome_item() == "copy-favoritos_23_12_2024.html"


def test_get_nome_pasta_mae(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    assert model.get_nome_pasta_mae() == "Chrome"


def test_to_dict(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    expected_dict = {
        "caminho_original": setup_paths["absolute_file_path"],
        "caminho_absoluto": str(Path(setup_paths["absolute_file_path"]).resolve()),
        "existe": True,
        "tipo_caminho": "absoluto",
        "tipo_item": "arquivo",
        "nome_item": "copy-favoritos_23_12_2024.html",
        "nome_pasta_mae": "Chrome",
    }
    assert model.to_dict() == expected_dict


def test_to_json(setup_paths):
    model = BasePathModel(setup_paths["absolute_file_path"])
    expected_json = json.dumps(
        model.to_dict(), indent=4, ensure_ascii=False, sort_keys=True
    )
    assert model.to_json() == expected_json
