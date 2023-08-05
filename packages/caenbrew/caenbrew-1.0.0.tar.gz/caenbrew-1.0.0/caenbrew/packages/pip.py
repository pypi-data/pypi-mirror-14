from ..packaging import package, SymlinkPackage


@package
class PipPackage(SymlinkPackage):
    """Pip is a package manager for Python."""

    name = "pip"
    homepage = "https://pypi.python.org/pypi/pip"
    version = "6.0.8"
    symlinks = {
        "/usr/um/python-2.7/bin/pip": "bin/pip",
    }
