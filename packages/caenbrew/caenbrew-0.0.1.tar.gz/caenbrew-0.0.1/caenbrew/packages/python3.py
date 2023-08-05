from ..packaging import package, SymlinkPackage


@package
class Python3Package(SymlinkPackage):
    """Python is a general-purpose dynamic scripting language."""

    name = "python3"
    version = "3.4.3"
    symlinks = {
        "/usr/um/python-3.4/bin/python3": "bin/python3",
        "/usr/um/python-3.4/bin/pip": "bin/pip3",
    }
