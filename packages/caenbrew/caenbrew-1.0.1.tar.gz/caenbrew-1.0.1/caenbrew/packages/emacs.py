from ..packaging import ConfigurePackage, package


@package
class EmacsPackage(ConfigurePackage):
    """emacs - GNU project Emacs."""

    name = "emacs"
    homepage = "https://www.gnu.org/software/emacs/"
    version = "24.5"
    artifacts = ["bin/emacs"]

    url = "http://ftp.wayne.edu/gnu/emacs/emacs-24.5.tar.xz"
    configure_options = ["--with-xpm=no",
                         "--with-gif=no",
                         "--with-tiff=no"]
