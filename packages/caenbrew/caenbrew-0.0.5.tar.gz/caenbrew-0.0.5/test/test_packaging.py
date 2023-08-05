import pytest

from caenbrew.packaging import (
    BasePackage,
    is_package,
    package,
)

CONFIG = {}
"""Example config to pass to a `BasePackage`."""


def test_package_decorator():
    """Ensure that we can mark packages and detect them."""
    class NotAPackage(object):
        pass

    @package
    class SomePackage(object):
        pass

    assert not is_package(NotAPackage)
    assert is_package(SomePackage)


def test_base_package_needs_name():
    """Ensure that a `BasePackage` subclass must have a name."""
    class WithName(BasePackage):
        name = "foo"

    class WithoutName1(BasePackage):
        pass

    class WithoutName2(BasePackage):
        name = None

    WithName(CONFIG)
    with pytest.raises(AttributeError):
        WithoutName1(CONFIG)
    with pytest.raises(AssertionError):
        WithoutName2(CONFIG)


class TestBasePackage(object):
    """Test the base package stubs."""

    def setup_method(self, method):
        """Create a `BasePackage`."""
        class TestingPackage(BasePackage):
            name = "testing-package"
        self.package = TestingPackage(CONFIG)

    def test_abstract_is_installed(self):
        """Ensure that `is_installed` is an abstract method."""
        with pytest.raises(NotImplementedError):
            self.package.is_installed

    @pytest.mark.parametrize("method_name", [
        "install",
        "uninstall",
    ])
    def test_abstract_methods(self, method_name):
        """Ensure that the specified methods are abstract."""
        with pytest.raises(NotImplementedError):
            getattr(self.package, method_name)()

    def test_noop_prepare(self):
        """Ensure that `prepare` is a no-op context manager."""
        with self.package.prepare():
            pass

    def test_noop_download(self):
        """Ensure that `download` is a no-op."""
        self.package.download()
