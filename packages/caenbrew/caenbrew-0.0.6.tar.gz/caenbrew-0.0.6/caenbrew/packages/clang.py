import os.path

from .cmake import CmakePackage

from ..packaging import ArtifactPackage, package, TempDirMixin


@package
class ClangPackage(TempDirMixin, ArtifactPackage):
    """The Clang front-end for LLVM.

    Also includes clang tools such as clang-format.
    """

    name = "clang"
    homepage = "http://clang.llvm.org/"
    version = "3.8.0"

    dependencies = [CmakePackage]

    # These aren't all the things that are installed, but a few things of
    # interest.
    artifacts = ["bin/clang",
                 "bin/clang-check",
                 "bin/clang-format",
                 "bin/scan-build"]

    _LLVM_URL = "http://llvm.org/releases/3.8.0/llvm-3.8.0.src.tar.xz"
    _LLVM_ARCHIVE_FILE = os.path.basename(_LLVM_URL)
    _CLANG_URL = "http://llvm.org/releases/3.8.0/cfe-3.8.0.src.tar.xz"
    _CLANG_ARCHIVE_FILE = os.path.basename(_CLANG_URL)

    _LLVM_DIR = "llvm"
    """Directory to extract the source code of LLVM to."""

    _CLANG_DIR = "llvm/tools/clang"
    """Directory to extract the source code of Clang to.

    Clang must be extracted into "llvm/tools" for the LLVM build system to
    detect it automatically.
    """

    def download(self):
        """Download and extract the LLVM and Clang source code."""
        self._cmd("curl", self._LLVM_URL, "-o", self._LLVM_ARCHIVE_FILE,
                  title="Downloading LLVM")
        self._cmd("curl", self._CLANG_URL, "-o", self._CLANG_ARCHIVE_FILE,
                  title="Downloading Clang")

        self._cmd("mkdir", "-p", self._LLVM_DIR)
        self._cmd("tar", "-xf", self._LLVM_ARCHIVE_FILE,
                  "-C", self._LLVM_DIR, "--strip-components", "1",
                  title="Extracting LLVM")

        self._cmd("mkdir", "-p", self._CLANG_DIR)
        self._cmd("tar", "-xf", self._CLANG_ARCHIVE_FILE,
                  "-C", self._CLANG_DIR, "--strip-components", "1",
                  title="Extracting Clang")

    def install(self):
        """Install LLVM, Clang, and the clang tools."""
        self._cmd("mkdir", "build")
        os.chdir("build")
        self._cmd("cmake", "-G", "Unix Makefiles", "../llvm",

                  # Release build. The debug build is said to take 15-20 GB of
                  # space, while the release build takes ~1 GB of space on my
                  # local machine. The CAEN quota is 10 GB.
                  "-DCMAKE_BUILD_TYPE=Release",

                  "-DCMAKE_INSTALL_PREFIX={}"
                  .format(self._config["prefix_dir"]),

                  title="Configuring package")

        self._cmd("make", "-j8", title="Building package")
        self._cmd("make", "install", title="Installing package")


@package
class LlvmPackage(ArtifactPackage):
    """LLVM: A modular compiler infrastructure.

    This package just installs LLVM+Clang via the 'clang' package.
    """

    name = "llvm"
    homepage = "http://llvm.org/"
    version = ClangPackage.version
    dependencies = [ClangPackage]
    artifacts = ClangPackage.artifacts
