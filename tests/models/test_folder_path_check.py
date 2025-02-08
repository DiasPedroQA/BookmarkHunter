# pylint: disable=C0114, C0115, C0116, E0401

from pathlib import Path
import pytest # type: ignore
from app.models.folder_path_check import FolderPathCheck


@pytest.fixture
def folder_path_checker_instance(mocker):
    mock_path = mocker.MagicMock(spec=Path)
    return FolderPathCheck(mock_path)


def test_is_a_real_folder(folder_path_check_instance: FolderPathCheck, mocker):
    folder_path_check_instance.path.exists.return_value = True
    folder_path_check_instance.path.is_dir.return_value = True
    folder_path_check_instance.path.is_file.return_value = False
    folder_path_check_instance.path.is_symlink.return_value = False
    folder_path_check_instance.is_readable = mocker.MagicMock(return_value=True)
    folder_path_check_instance.is_writable = mocker.MagicMock(return_value=True)
    folder_path_check_instance.is_not_empty_folder = mocker.MagicMock(return_value=True)

    assert folder_path_check_instance.is_a_real_folder()


def test_is_not_empty_folder(folder_path_check_instance: FolderPathCheck, mocker):
    folder_path_check_instance.path.iterdir.return_value = [mocker.MagicMock()]
    assert folder_path_check_instance.is_not_empty_folder()


def test_list_files(folder_path_check_instance: FolderPathCheck, mocker):
    mock_file = mocker.MagicMock()
    mock_file.is_file.return_value = True
    folder_path_check_instance.path.iterdir.return_value = [mock_file]

    assert folder_path_check_instance.list_files() == [mock_file]


def test_get_folder_size(folder_path_check_instance: FolderPathCheck, mocker):
    mock_file = mocker.MagicMock()
    mock_file.is_file.return_value = True
    mock_file.stat.return_value.st_size = 1024
    folder_path_check_instance.path.iterdir.return_value = [mock_file]

    assert folder_path_check_instance.get_folder_size() == 1024
