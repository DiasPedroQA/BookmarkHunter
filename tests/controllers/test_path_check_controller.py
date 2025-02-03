# pylint: disable=C0114, C0115, C0116, E0401

from unittest.mock import patch
import pytest
from app.controllers.path_check_controller import PathCheckController


@pytest.fixture
def path_mock_check():
    with patch("app.controllers.path_check_controller.PathCheck") as mock_path_check:
        yield mock_path_check.return_value


@pytest.fixture
def controller():
    return PathCheckController("/fake/path")


def test_check_exists(ctrl: PathCheckController, mock_path_check):
    mock_path_check.path_exists.return_value = True
    assert ctrl.check_exists()
    mock_path_check.path_exists.assert_called_once()


def test_is_readable_and_writable(ctrl: PathCheckController, mock_path_check):
    mock_path_check.is_readable.return_value = True
    mock_path_check.is_writable.return_value = True
    assert ctrl.is_readable_and_writable()
    mock_path_check.is_readable.assert_called_once()
    mock_path_check.is_writable.assert_called_once()


def test_is_not_symlink(ctrl: PathCheckController, mock_path_check):
    mock_path_check.is_not_symlink.return_value = True
    assert ctrl.is_not_symlink()
    mock_path_check.is_not_symlink.assert_called_once()


def test_get_absolute_path(ctrl: PathCheckController, mock_path_check):
    mock_path_check.get_absolute_path.return_value = "/absolute/path"
    assert ctrl.get_absolute_path() == "/absolute/path"
    mock_path_check.get_absolute_path.assert_called_once()


def test_get_path_timing(ctrl: PathCheckController, mock_path_check):
    mock_path_check.get_creation_time.return_value = "2023-01-01"
    mock_path_check.get_modification_time.return_value = "2023-01-02"
    mock_path_check.get_access_time.return_value = "2023-01-03"
    expected_timing = {
        "path_creation_time": "2023-01-01",
        "path_modification_time": "2023-01-02",
        "path_access_time": "2023-01-03",
    }
    assert ctrl.get_path_timing() == expected_timing
    mock_path_check.get_creation_time.assert_called_once()
    mock_path_check.get_modification_time.assert_called_once()
    mock_path_check.get_access_time.assert_called_once()


def test_validate_path_success(ctrl: PathCheckController, mock_path_check):
    mock_path_check.path_exists.return_value = True
    mock_path_check.is_readable.return_value = True
    mock_path_check.is_writable.return_value = True
    mock_path_check.is_not_symlink.return_value = True
    assert ctrl.validate_path()


def test_validate_path_not_exists(ctrl: PathCheckController, mock_path_check):
    mock_path_check.path_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        ctrl.validate_path()


def test_validate_path_not_readable_writable(ctrl: PathCheckController, mock_path_check):
    mock_path_check.path_exists.return_value = True
    mock_path_check.is_readable.return_value = False
    mock_path_check.is_writable.return_value = True
    with pytest.raises(PermissionError):
        ctrl.validate_path()


def test_validate_path_is_symlink(ctrl: PathCheckController, mock_path_check):
    mock_path_check.path_exists.return_value = True
    mock_path_check.is_readable.return_value = True
    mock_path_check.is_writable.return_value = True
    mock_path_check.is_not_symlink.return_value = False
    with pytest.raises(ValueError):  # Assuming ValueError is raised for symlink
        ctrl.validate_path()
