# pylint: disable=C0114, C0115, C0116, E0401

from unittest.mock import MagicMock
import pytest # type: ignore
from app.controllers.folder_path_check_controller import FolderPathCheckController


@pytest.fixture
def folder_mock_path_check(mocker):
    mock = MagicMock()
    mocker.patch("app.controllers.folder_path_check_controller.FolderPathCheck", return_value=mock)
    return mock


@pytest.fixture
def path_controller():
    return FolderPathCheckController("/fake/path")


def test_validate_folder_valid(mock_folder_path_check, controller):
    mock_folder_path_check.is_a_real_folder.return_value = True
    result = controller.validate_folder()
    assert result


def test_validate_folder_invalid(mock_folder_path_check, controller):
    mock_folder_path_check.is_a_real_folder.return_value = False
    with pytest.raises(ValueError):
        controller.validate_folder()


def test_is_a_real_folder(mock_folder_path_check, controller):
    mock_folder_path_check.is_a_real_folder.return_value = True
    result = controller.is_a_real_folder()
    assert result


def test_is_readable(mock_folder_path_check, controller):
    mock_folder_path_check.is_readable.return_value = True
    result = controller.is_readable()
    assert result


def test_is_writable(mock_folder_path_check, controller):
    mock_folder_path_check.is_writable.return_value = True
    result = controller.is_writable()
    assert result


def test_is_empty(mock_folder_path_check, controller):
    mock_folder_path_check.is_not_empty_folder.return_value = False
    result = controller.is_empty()
    assert not result
