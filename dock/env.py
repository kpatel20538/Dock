from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

from dock import files, config


class BuildEnvironment:
    def __init__(self, directory: Path):
        self.directory = files.expand(directory)

    def __hash__(self) -> int:
        return hash(self.directory)

    def __eq__(self, other: "BuildEnvironment") -> bool:
        return self.directory == other.directory

    @property
    @lru_cache()
    def dockerfile(self) -> Path:
        return self.directory / 'Dockerfile'

    @property
    @lru_cache()
    def configfile(self) -> Path:
        return self.directory / 'image_config.json'

    def touch(self):
        """ Ensure a basic build environment exists """
        self.directory.mkdir(exist_ok=True, parents=True)
        if not self.dockerfile.exists():
            with self.dockerfile.open('w') as df:
                df.write('FROM x11docker/lxqt')
        if not self.configfile.exists():
            config.dump_default(self.configfile)
        return self

    def remove(self):
        files.remove_directory(self.directory)

    @contextmanager
    def as_working_directory(self):
        """Change the current working directory for a block of code"""
        with files.current_working_directory(self.directory):
            yield


def save(source_env: BuildEnvironment, cache_env: BuildEnvironment):
    files.copy_directory(source_env.directory, cache_env.directory)
    files.clear_compare_cache()


def are_same(source_env: BuildEnvironment, cache_env: BuildEnvironment):
    return files.are_same(source_env.directory, cache_env.directory)