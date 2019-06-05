import filecmp
import os
import shutil
from contextlib import contextmanager
from pathlib import Path

from typing import Union

# noinspection PyUnresolvedReferences
from sh import xdg_open


def fix(target: Path) -> str:
    """Convert path to str. Str will represent an absolute path with home directory resolved"""
    return str(expand(target))

def expand(target: Union[Path, str]) -> Path:
    """Expand path into absolute path with home directory resolved"""
    return Path(target).expanduser().absolute()

def clear_compare_cache():
    """Invalidate File Comparison Cache: Invoke if their is a known file change"""
    return filecmp.clear_cache()


def are_same(source: Path, target: Path) -> bool:
    """Compare is the contents of two files/directories are are the same.
    Useful for testing if a image re-build is needed.
    """
    source, target = expand(source), expand(target)
    if source.is_dir() and target.is_dir():
        cmp = filecmp.dircmp(fix(source), fix(target))
        return not (cmp.left_only or cmp.right_only or cmp.diff_files)
    elif source.is_file() and target.is_file():
        return filecmp.cmp(fix(source), fix(target))
    else:
        return False


def copy_directory(source: Path, target: Path):
    def copy(src, dst, _=True):
        return shutil.copy(src, dst, follow_symlinks=False)

    remove_directory(target)
    shutil.copytree(fix(source), fix(target), symlinks=True,
                    copy_function=copy)


def move_directory(source: Path, target: Path):
    source, target = expand(source), expand(target)
    source.replace(target)


def remove_directory(target: Path):
    target = expand(target)
    if target.exists():
        if target.is_dir():
            shutil.rmtree(fix(target))
        else:
            target.unlink()


@contextmanager
def current_working_directory(target: Path):
    """Change the current working directory for a block of code"""
    old_cwd = Path.cwd()
    os.chdir(fix(target))
    yield
    os.chdir(fix(old_cwd))


def make_archive(archive: Path, source: Path, archive_format='gztar'):
    shutil.make_archive(fix(archive), archive_format, fix(source))


def unpack_archive(archive: Path, target: Path, archive_format='gztar'):
    shutil.unpack_archive(fix(archive), fix(target), archive_format)


def open_resource(target: Path):
    """ Opens a resource file in it's preferred application """
    xdg_open(fix(target))
