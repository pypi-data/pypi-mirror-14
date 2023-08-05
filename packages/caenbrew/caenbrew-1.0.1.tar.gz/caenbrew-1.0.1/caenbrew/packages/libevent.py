from ..packaging import ConfigurePackage, package


@package
class LibeventPackage(ConfigurePackage):
    """Libevent: An event notification library."""

    name = "libevent"
    homepage = "http://libevent.org/"
    version = "2.0.22"

    artifacts = ["include/event2", "lib/libevent.a", "lib/libevent.so"]
    url = "https://github.com/libevent/libevent/releases/download/release-2.0.22-stable/libevent-2.0.22-stable.tar.gz"  # noqa
