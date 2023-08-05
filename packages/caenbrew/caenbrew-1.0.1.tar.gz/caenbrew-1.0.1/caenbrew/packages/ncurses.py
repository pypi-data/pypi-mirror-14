from ..packaging import ConfigurePackage, package


@package
class NcursesPackage(ConfigurePackage):
    """ncurses: An event notification library."""

    name = "ncurses"
    homepage = "http://invisible-island.net/ncurses/"
    version = "5.9"

    artifacts = ["include/ncurses", "lib/libncurses.a"]
    url = "ftp://invisible-island.net/ncurses/ncurses.tar.gz"

    configure_options = [
        # Doesn't build on AFS:
        # https://groups.google.com/forum/#!topic/sage-devel/1F0b6Zpb4k0
        "--enable-symlinks",

        # Doesn't build under GCC 5.x: http://trac.sagemath.org/ticket/18301
        # Use system GCC and assume that it's suitably low-versioned (currently
        # 4.8.5).
        "CC=/usr/bin/gcc",
    ]
