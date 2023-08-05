from ..packaging import ConfigurePackage, package


@package
class VimPackage(ConfigurePackage):
    """VIM - Vi IMproved."""

    name = "vim"
    homepage = "http://www.vim.org/"
    version = "7.4"
    artifacts = ["bin/vim"]

    url = "ftp://ftp.vim.org/pub/vim/unix/vim-7.4.tar.bz2"
    configure_options = ["--enable-multibyte",
                         "--enable-pythoninterp=yes"]
