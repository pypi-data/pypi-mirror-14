import os

from ..packaging import ConfigurePackage, package


@package
class CppcheckPackage(ConfigurePackage):
    """Cppcheck is a static analysis tool for C/C++ code."""

    name = "cppcheck"
    homepage = "http://cppcheck.sourceforge.net/"
    version = "1.72"
    artifacts = ["bin/cppcheck"]

    url = "http://downloads.sourceforge.net/project/cppcheck/cppcheck/1.72/cppcheck-1.72.tar.bz2"  # noqa

    def install(self):
        """Install with `make` invocations only."""
        os.chdir(self._ARCHIVE_DIR)

        self._cmd("make", title="Building package")
        self._cmd("make",
                  "PREFIX={}".format(self._config["prefix_dir"]),
                  "install",
                  title="Installing package")
