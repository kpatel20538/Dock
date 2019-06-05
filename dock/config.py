import json
from functools import lru_cache
from pathlib import Path
from typing import List

from dock import files


def default_label() -> str:
    return 'io.github.x11docker'


class Config:
    def __init__(self, x11docker_flags, docker_run_flags, build_flags):
        self.x11docker_flags = tuple(x11docker_flags)
        self.docker_run_flags = tuple(docker_run_flags)
        self.build_flags = tuple(build_flags)

    def __hash__(self) -> int:
        return hash((self.x11docker_flags, self.docker_run_flags, self.build_flags))

    def __eq__(self, other: "Config") -> bool:
        return (self.x11docker_flags, self.docker_run_flags, self.build_flags) == \
               (other.x11docker_flags, other.docker_run_flags, other.build_flags)

    @property
    @lru_cache()
    def run_flags(self):
        return self.x11docker_flags + ("--",) + self.docker_run_flags


def load(configfile: Path, image_directory: Path, tag: str, force=False) -> Config:
    with files.expand(configfile).open('r') as cf:
        config = json.load(cf)

    def format_flags(flags: List[str]) -> List[str]:
        return [flag.format(
            user_home=files.fix(Path.home()),
            image_dir=files.fix(image_directory),
            image_tag=tag,
            default_label=default_label()
        ) for flag in flags]

    build_flags = config.get('dockerBuildFlags', [])
    build_flags.extend(['--rm', '--tag={image_tag}', '--label={default_label}'])
    if force:
        build_flags.append('--no-cache')

    return Config(
        format_flags(config.get('x11dockerFlags', [])),
        format_flags(config.get('dockerRunFlags', [])),
        format_flags(build_flags),
    )


def dump_default(configfile: Path):
    with files.expand(configfile).open('w') as cf:
        json.dump({
            'x11dockerFlags': ['--homedir={image_dir}/home', '--desktop', '--pulseaudio'],
            'dockerRunFlags': ['--privileged'],
            'dockerBuildFlags': [],
        }, cf, indent=4, sort_keys=True)
