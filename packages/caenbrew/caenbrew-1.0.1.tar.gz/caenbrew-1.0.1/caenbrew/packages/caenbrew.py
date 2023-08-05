from ..packaging import BasePackage, package


@package
class CaenbrewPackage(BasePackage):
    """Caenbrew: the best CAEN package manager around."""

    name = "caenbrew"
    homepage = "https://github.com/arxanas/caenbrew"

    # TODO: Actually get the correct version here.
    version = "0.0.0"

    _CAENBREW_GIT_URL = "git+git://github.com/arxanas/caenbrew.git"
    """The Git URL to install from via Pip.

    By pointing to the actual Git repo, we can update packages without pushing
    a new version to PyPI. (The disadvantage is that people can get stuck with
    a non-working Caenbrew.)
    """

    @property
    def is_installed(self):
        """If this code runs, then Caenbrew is installed."""
        return True

    def install(self):
        """If the user tries to force a reinstall, instead try an upgrade."""
        self._cmd("/usr/um/python-2.7/bin/pip",
                  "install", "--upgrade", self._CAENBREW_GIT_URL,
                  "--user",
                  title="Upgrading caenbrew")

    def uninstall(self):
        """Uninstall Caenbrew.

        You can bet that some people will try this and be surprised when it
        works ;)
        """
        self._cmd("/usr/um/python-2.7/bin/pip", "uninstall", "-y", "caenbrew",
                  title="Uninstalling caenbrew")
