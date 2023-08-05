from .libevent import LibeventPackage
from .ncurses import NcursesPackage

from ..packaging import ConfigurePackage, package


@package
class TmuxPackage(ConfigurePackage):
    """tmux is a terminal multiplexer."""

    name = "tmux"
    homepage = "https://tmux.github.io/"
    version = "2.1"
    dependencies = [LibeventPackage, NcursesPackage]

    artifacts = ["bin/tmux"]
    url = "https://github.com/tmux/tmux/releases/download/2.1/tmux-2.1.tar.gz"

    def __init__(self, *args, **kwargs):
        """Set configure options to work around tmux not finding libevent."""
        super(TmuxPackage, self).__init__(*args, **kwargs)

        # http://unix.stackexchange.com/a/17918/24718
        prefix_dir = self._config["prefix_dir"]
        self.configure_options = ["CFLAGS=-I{}/include".format(prefix_dir),
                                  "LDFLAGS=-L{}/lib".format(prefix_dir)]
