from ..packaging import BasePackage, InstallFailure, package


@package
class CaenbrewPackage(BasePackage):
    """Package to represent Caenbrew, which can't be managed by Caenbrew."""

    name = "caenbrew"

    @property
    def is_installed(self):
        """Caenbrew is always installed."""
        return True

    def install(self):
        """Warn the user that Caenbrew is always installed."""
        raise InstallFailure("You can't manage Caenbrew with Caenbrew!")

    def uninstall(self):
        """No-op."""
