from typing import Optional

from sh import ErrorReturnCode
# noinspection PyUnresolvedReferences
from sh.contrib import sudo
# noinspection PyUnresolvedReferences
from sh import docker, x11docker, systemctl


def ensure_service() -> bool:
    """Poke SystemD to ensure docker is running"""
    try:
        systemctl('is-active', 'docker', _fg=True)
        return False
    except ErrorReturnCode:
        systemctl.start('docker', _fg=True)
        return True


def build(*args):
    """ Build Image in the Current Working Directory """
    with sudo:
        ensure_service()
        docker.build('.', *args, _fg=True)


def run(tag: str, *args):
    """ Run Image in the Current Working Directory """
    with sudo:
        ensure_service()
        x11docker(*args, '--', tag, _fg=True)


def remove_image(tag: str):
    with sudo:
        docker.rmi(tag, _fg=True)


def prune(label: Optional[str] = None):
    """ Deletes dangling images and exited containers """
    with sudo:
        if label is None:
            docker.container.prune(_fg=True)
            docker.image.prune(_fg=True)
        else:
            docker.container.prune(filter='label={}'.format(label), _fg=True)
            docker.image.prune(filter='label={}'.format(label), _fg=True)


def list_containers(label: Optional[str] = None):
    """ Lists Docker Containers """
    with sudo:
        if label is None:
            docker.ps(_fg=True)
        else:
            docker.ps(filter='label={}'.format(label), _fg=True)


def stop_container(container: str, time: int = 10):
    """ Stop a Docker Container by ID"""
    with sudo:
        docker.stop(container, time=time, _fg=True)
