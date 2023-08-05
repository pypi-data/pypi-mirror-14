from ..packaging import ConfigurePackage, package


@package
class CmakePackage(ConfigurePackage):
    """Cmake is an open-source, cross-platform family of build tools."""

    name = "cmake"
    homepage = "https://cmake.org/"
    version = "3.5.0"
    artifacts = ["bin/cmake"]

    url = "https://cmake.org/files/v3.5/cmake-3.5.0.tar.gz"
