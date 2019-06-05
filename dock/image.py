from functools import lru_cache
from pathlib import Path
from typing import Union

from dock import files, docker, config, env


class Image:
    def __init__(self, images: Union[str, Path], tag: str):
        self.directory = files.expand(images) / tag.replace('/', '#')
        self.tag = tag

    def __repr__(self):
        return self.tag

    def __hash__(self) -> int:
        return hash((self.directory, self.tag))

    def __eq__(self, other: "Image") -> bool:
        return (self.directory, self.tag) == (other.directory, other.tag)

    @property
    @lru_cache()
    def build_env(self) -> env.BuildEnvironment:
        return env.BuildEnvironment(self.directory / 'build')

    @property
    @lru_cache()
    def cache_env(self) -> env.BuildEnvironment:
        return env.BuildEnvironment(self.directory / '.build_cache')

    def touch(self):
        self.build_env.touch()
        return self

    def clean(self):
        self.cache_env.remove()
        files.clear_compare_cache()
        return self

    def remove(self):
        docker.remove_image(self.tag)
        files.remove_directory(self.directory)
        return self

    def backup(self, archive: str):
        """ Make an archive of an image """
        files.make_archive(Path(archive), self.directory)
        return self

    def restore(self, archive: str):
        """ Restore an image from an archive """
        files.unpack_archive(Path(archive), self.directory)
        return self

    def exists(self):
        return self.directory.exists()

    def build(self, force: bool = False, suggest: bool = False):
        """ Conditionally build the image with docker, checking/caching the build files """
        if suggest or force or not env.are_same(self.build_env, self.cache_env):
            configfile = self.build_env.configfile
            cfg = config.load(configfile, self.directory, self.tag, force=force)
            with self.build_env.as_working_directory():
                docker.build(*cfg.build_flags)
            env.save(self.build_env, self.cache_env)
        return self

    def run(self):
        """ Running the image with x11docker """
        cfg = config.load(self.build_env.configfile, self.directory, self.tag)
        with self.build_env.as_working_directory():
            docker.run(self.tag, *cfg.run_flags)
        return self
