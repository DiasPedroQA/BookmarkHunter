# pylint: disable=C0114, C0115, C0116, E0401

import os
import tempfile
from pathlib import Path
from app.models.path_check import PathCheck


def test_path_exists():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.path_exists() is True

def test_path_does_not_exist():
    path_check = PathCheck("/non/existent/path")
    assert path_check.path_exists() is False

def test_is_not_symlink():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.is_not_symlink() is True

def test_is_symlink():
    with tempfile.TemporaryDirectory() as temp_dir:
        symlink_path = os.path.join(temp_dir, "symlink")
        os.symlink(temp_dir, symlink_path)
        path_check = PathCheck(symlink_path)
        assert path_check.is_not_symlink() is False

def test_get_absolute_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.get_absolute_path() == Path(temp_dir).resolve()

def test_get_metadata():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.get_metadata() is not None

def test_is_readable():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.is_readable() is True

def test_is_writable():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.is_writable() is True

def test_get_creation_time():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.get_creation_time() is not None

def test_get_modification_time():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.get_modification_time() is not None

def test_get_access_time():
    with tempfile.TemporaryDirectory() as temp_dir:
        path_check = PathCheck(temp_dir)
        assert path_check.get_access_time() is not None
