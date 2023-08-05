from ..packaging import ConfigurePackage, package


@package
class FishPackage(ConfigurePackage):
    """fish is a smart and user-friendly command line shell."""

    name = "fish"
    version = "2.2.0"
    artifacts = ["bin/fish"]

    url = "https://fishshell.com/files/2.2.0/fish-2.2.0.tar.gz"
