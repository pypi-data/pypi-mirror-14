import contextlib
import os
import shutil
import subprocess
import tempfile

import click


def package(cls):
    """Decorator to denote that a class is a package.

    :param object cls: The class to mark as a package.
    """
    setattr(cls, "_is_package", True)
    return cls


def is_package(cls):
    """Determine whether the given class is a package.

    :param object cls: The class to check.
    :returns bool: Whether or not the class is a package.
    """
    return getattr(cls, "_is_package", False)


class InstallFailure(RuntimeError):
    """Raised when an installation fails."""


class BasePackage(object):
    """The base package installation class.

    The following variables should be defined by subclasses.

    :ivar str name: Required. The name of the package.
    """

    def __init__(self, config):
        """Initialize with the given configuration.

        :param dict config: The `caenbrew` configuration.
        """
        self._config = config

        assert self.name

    @property
    def is_installed(self):
        """Whether or not this package is installed.

        Must be overridden by subclasses.
        """
        raise NotImplementedError()

    @contextlib.contextmanager
    def prepare(self):
        """Prepare to install the package.

        No-op; should be overridden by subclasses. This function should be a
        context manager.
        """
        yield

    def download(self):
        """Download the package source.

        No-op; should be overridden by subclasses.
        """
        pass

    def install(self):
        """Install the package.

        Must be overridden by subclasses.
        """
        raise NotImplementedError()

    def uninstall(self):
        """Uninstall the package.

        Must be overridden by subclasses.
        """
        raise NotImplementedError()

    def _cmd(self, *command, **kwargs):
        """Run the specified command in a subprocess.

        :param list command: The space-separated words in the command to run,
            as you would type it on the command line.
        :param str title: The title of this command.
        """
        title = kwargs.get("title")
        if title:
            click.echo("{}... ({})"
                       .format(click.style("==> " + title, bold=True),
                               " ".join(command)))

        if not self._config["verbose"]:
            with open(os.devnull, "w") as devnull:
                return_code = subprocess.call(command, stdout=devnull)
        else:
            return_code = subprocess.call(command)

        if return_code != 0:
            raise RuntimeError("Command '{}' failed".format(command[0]))


class ArtifactPackage(BasePackage):
    """A package with artifacts and a version.

    The following variables should be defined by subclasses.

    :ivar str version: Required. The version of the package.
    :ivar list artifacts: Required. A list of files installed by the package.
        This is used to determine if the package is installed.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the package.

        Verify that the subclass has set the appropriate fields.
        """
        super(ArtifactPackage, self).__init__(*args, **kwargs)
        assert self.version
        assert self.artifacts

    @property
    def is_installed(self):
        """Determine whether this package is installed.

        :returns bool: Whether or not the package is installed.
        """
        def is_artifact_installed(artifact):
            return os.path.exists(self._artifact_path(artifact))
        return all(is_artifact_installed(i) for i in self.artifacts)

    def uninstall(self):
        """Remove the package artifacts."""
        self._cmd("rm", "-r",
                  *[self._artifact_path(i) for i in self.artifacts],
                  title="Removing artifacts")

    def _artifact_path(self, artifact):
        """Get the path to a given artifact.

        :param str artifact: The artifact.
        :returns str: The full path to that artifact.
        """
        return os.path.join(self._config["prefix_dir"], artifact)


class ConfigurePackage(ArtifactPackage):
    """Install a package with a configure-make-make install loop.

    The following variables should be defined by subclasses.

    :ivar str url: Required. The URL from which we can download the package.
    :ivar list configure_options: Optional. A list of arguments to pass to
        `configure`.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the ConfigurePackage."""
        super(ConfigurePackage, self).__init__(*args, **kwargs)

        assert self.url

    _ARCHIVE_DIR = "package_contents"
    """The directory to extract the archive into."""

    @contextlib.contextmanager
    def prepare(self):
        """Set up the working directory to use for installation."""
        self._temp_dir = tempfile.mkdtemp()
        os.chdir(self._temp_dir)
        yield
        shutil.rmtree(self._temp_dir)

    def download(self):
        """Make a temporary directory and unpack the archive there."""
        archive_file = os.path.basename(self.url)

        self._cmd("curl", self.url,
                  "--output", archive_file,
                  title="Downloading {}".format(self.name))
        self._cmd("mkdir", "-p", self._ARCHIVE_DIR)
        self._cmd("tar",
                  "-xf", archive_file,
                  "-C", self._ARCHIVE_DIR,
                  "--strip-components", "1",
                  title="Extracting package")

    def install(self):
        """Configure, build, and install the package."""
        os.chdir(self._ARCHIVE_DIR)

        configure_options = getattr(self, "configure_options", {})
        self._cmd("./configure",
                  "--prefix", self._config["prefix_dir"],
                  *configure_options,
                  title="Configuring package")

        self._cmd("make", title="Building package")
        self._cmd("make", "install", title="Installing package")


class SymlinkPackage(ArtifactPackage):
    """A package which can be installed by symlinking files into place.

    Subclasses may opt to omit the definition of `artifacts`. In this case, it
    is inferred from the symlinks.

    The following variables should be defined by subclasses.

    :ivar dict symlinks: A mapping from source files to destination files.
    """

    def __init__(self, *args, **kwargs):
        """Verify that there are symlinks for this package."""
        assert self.symlinks

        # Assume that the artifacts are the things we are symlinking to.
        if not getattr(self, "artifacts", None):
            self.artifacts = self.symlinks.values()

        super(SymlinkPackage, self).__init__(*args, **kwargs)

    def install(self):
        """Symlink all the files into place."""
        for source, dest in self.symlinks.iteritems():
            self._cmd("ln", "-s", source, self._artifact_path(dest),
                      title="Installing {}".format(os.path.basename(dest)))
