# pylint: disable=C0114, C0115, C0116, E0401

from pathlib import Path
from typing import Any
import pytest
from app.models.file_path_check import FilePathCheck


@pytest.fixture
def file_path_checker(mocker):
    mock_path = mocker.MagicMock(spec=Path)
    return FilePathCheck(mock_path), mock_path


def test_is_a_real_file(file_path_check: tuple[FilePathCheck, Any]):
    file_path_check_instance, mock_path = file_path_check
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.is_symlink.return_value = False
    file_path_check_instance.is_readable = lambda: True
    file_path_check_instance.is_writable = lambda: True
    file_path_check_instance.has_valid_extension = lambda: True
    file_path_check_instance.is_not_empty = lambda: True

    assert file_path_check_instance.is_a_real_file()


def test_has_valid_extension(file_path_check: tuple[FilePathCheck, Any]):
    file_path_check_instance, mock_path = file_path_check
    mock_path.suffix = ".html"
    assert file_path_check_instance.has_valid_extension()

    mock_path.suffix = ".txt"
    assert not file_path_check_instance.has_valid_extension()

    with pytest.raises(ValueError):
        file_path_check_instance.has_valid_extension(set())


def test_is_not_empty(file_path_check: tuple[FilePathCheck, Any]):
    file_path_check_instance, mock_path = file_path_check
    mock_path.stat.return_value.st_size = 10
    assert file_path_check_instance.is_not_empty()

    mock_path.stat.return_value.st_size = 0
    assert not file_path_check_instance.is_not_empty()


def test_get_file_size(file_path_check: tuple[FilePathCheck, Any]):
    file_path_check_instance, mock_path = file_path_check
    mock_path.is_file.return_value = True
    mock_path.stat.return_value.st_size = 1024
    assert file_path_check_instance.get_file_size() == 1024

    mock_path.is_file.return_value = False
    assert file_path_check_instance.get_file_size() == 0


def test_is_readable(file_path_check: tuple[FilePathCheck, Any]):
    file_path_check_instance, mock_path = file_path_check
    mock_path.stat.return_value.st_mode = 0o644
    assert file_path_check_instance.is_readable()

    mock_path.stat.return_value.st_mode = 0o200
    assert not file_path_check_instance.is_readable()


def test_is_writable(file_path_check: tuple[FilePathCheck, Any]):
    file_path_check_instance, mock_path = file_path_check
    mock_path.stat.return_value.st_mode = 0o644
    assert file_path_check_instance.is_writable()

    mock_path.stat.return_value.st_mode = 0o400
    assert not file_path_check_instance.is_writable()
