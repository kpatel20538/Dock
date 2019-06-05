import os
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union

from dock import image, files


class Repository:
    def __init__(self, directory: Optional[Union[str, Path]] = None):
        if directory is None:
            try:
                self.directory = files.expand(Path(os.environ['DOCK_DESKTOP_X11_HOME']))
            except KeyError:
                self.directory = files.expand(Path.home()) / '.local' / 'share' / 'dock'
        else:
            self.directory = files.expand(directory)
        self.images.mkdir(exist_ok=True, parents=True)

    def __hash__(self) -> int:
        return hash(self.directory)

    def __eq__(self, other: "Repository") -> bool:
        return self.directory == other.directory

    @property
    @lru_cache()
    def images(self) -> Path:
        return self.directory / 'images'

    @lru_cache()
    def __getitem__(self, tag: str) -> image.Image:
        try:
            return image.Image(self.images, tag)
        except ValueError:
            raise KeyError('{} IMAGE NOT FOUND'.format(tag))

    def __contains__(self, tag: str) -> bool:
        return self[tag].exists()

    def __iter__(self):
        for image_directory in files.expand(self.images).iterdir():
            tag = image_directory.name.replace('#', '/')
            yield image.Image(self.images, tag)
