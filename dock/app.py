from typing import Optional

from fire import Fire

from dock import files, docker, config, repository


def user_verify(prompt: str = "") -> bool:
    return input(prompt).lower() in {'y', 'yes'}


class App:
    def __init__(self, repo: Optional[str] = None):
        self._repo = repository.Repository(repo)

    def images(self):
        """Lists Available Images"""
        for image in self._repo:
            print("{tag} : {directory}".format(tag=image.tag, directory=image.directory))

    def containers(self):
        """Lists Containers"""
        docker.list_containers(label=config.default_label())

    def stop(self, container: str, time: int = 10):
        """Stops the given container"""
        docker.stop_container(container, time=time)

    def prune(self):
        """Unloads all exited containers and dangling images"""
        docker.prune(label=config.default_label())

    def image(self, tag: str):
        """Open the image's working directory in the default file manager"""
        files.open_resource(self._repo[tag].directory)

    def repository(self):
        """Open the repository's working directory in the default file manager"""
        files.open_resource(self._repo.directory)

    def dockerfile(self, tag: str):
        """Open the image's dockerfile in the default text editor"""
        files.open_resource(self._repo[tag].build_env.dockerfile)

    def configfile(self, tag: str):
        """Open the image's x11docker run configuration file in the default text editor"""
        files.open_resource(self._repo[tag].build_env.configfile)

    def touch(self, tag: str):
        """If no images exists, create a basic template for this tag"""
        self._repo[tag].touch()

    def clean(self, tag: str):
        """Remove the image's build cache"""
        self._repo[tag].clean()

    def move(self, source_tag: str, target_tag: str, only_build: bool = False):
        """ Relabel an image """
        source, target = self._repo[source_tag], self._repo[target_tag]
        if only_build:
            files.move_directory(source.build_env.directory, target.build_env.directory)
        else:
            files.move_directory(source.directory, target.directory)
        target.build(suggest=True)
        source.remove()

    def copy(self, source_tag: str, target_tag: str, only_build: bool = False):
        """ Duplicate an image"""
        source, target = self._repo[source_tag], self._repo[target_tag]
        if only_build:
            files.copy_directory(source.build_env.directory, target.build_env.directory)
        else:
            files.copy_directory(source.directory, target.directory)
        target.build(suggest=True)

    def remove(self, tag: str, force: bool = False):
        """Remove the image completely"""
        if force or user_verify("DELETE {} completely?\n[Y/N] $> ".format(tag)):
            self._repo[tag].remove()

    def backup(self, tag: str, archive: str):
        """ Make an archive of an image """
        self._repo[tag].backup(archive)

    def restore(self, tag: str, archive: str, force: bool = False):
        """ Restore an image from an archive """
        if tag not in self._repo or force or user_verify("DELETE and RESTORE {} completely?\n[Y/N] $> ".format(tag)):
            self._repo[tag].remove().restore(archive)

    def build(self, tag: str, force: bool = False, suggest: bool = False):
        """Build an image if necessary"""
        print("\nSTART\n")
        self._repo[tag].build(force, suggest)
        print("\nDONE\n")

    def run(self, tag: str, force: bool = False, suggest: bool = False):
        """Build an image if necessary and run it"""
        print("\nSTART\n")
        self._repo[tag].build(force, suggest).run()
        print("\nDONE\n")


def main():
    Fire(App)
