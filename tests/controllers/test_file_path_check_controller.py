# pylint: disable=C0114, C0115, C0116, E0401

from unittest.mock import patch
import pytest # type: ignore
from app.controllers.file_path_check_controller import FilePathCheckController


@pytest.fixture
@patch("models.file_path_check.FilePathCheck")
def mock_file_path_check():
    mock = mock_file_path_check.return_value
    mock.path.exists.return_value = True
    return mock


@pytest.fixture
def controller():
    return FilePathCheckController("/fake/path")


def test_init_raises_file_not_found_error():
    mock_file_path_check.path.exists.return_value = False
    with pytest.raises(FileNotFoundError):
        FilePathCheckController("/non/existent/path")


def test_is_a_real_file(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.is_a_real_file.return_value = True
    assert ctrl.is_a_real_file()
    mock_file_path_check_instance.is_a_real_file.assert_called_once()


def test_is_readable(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.is_readable.return_value = True
    assert ctrl.is_readable()
    mock_file_path_check_instance.is_readable.assert_called_once()


def test_is_writable(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.is_writable.return_value = True
    assert ctrl.is_writable()
    mock_file_path_check_instance.is_writable.assert_called_once()


def test_has_valid_extension(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.has_valid_extension.return_value = True
    assert ctrl.has_valid_extension([".txt", ".md"])
    mock_file_path_check_instance.has_valid_extension.assert_called_once_with([".txt", ".md"])


def test_is_not_empty(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.is_not_empty.return_value = True
    assert ctrl.is_not_empty()
    mock_file_path_check_instance.is_not_empty.assert_called_once()


def test_validate_file(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.is_a_real_file.return_value = True
    assert ctrl.validate_file()
    mock_file_path_check_instance.is_a_real_file.assert_called_once()


def test_validate_file_raises_value_error(ctrl: FilePathCheckController, mock_file_path_check_instance):
    mock_file_path_check_instance.is_a_real_file.return_value = False
    with pytest.raises(ValueError):
        ctrl.validate_file()
