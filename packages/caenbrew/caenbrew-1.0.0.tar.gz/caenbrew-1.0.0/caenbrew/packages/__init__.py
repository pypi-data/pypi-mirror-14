import importlib
import os.path
import pkgutil

from ..packaging import is_package


def load_packages(module):
    """Find all packages.

    :returns dict: A mapping of package name to package class.
    """
    path = os.path.dirname(module.__file__)
    loaded_packages = {}
    for i in pkgutil.iter_modules([path]):
        _, name, is_package = i

        # It's not a module, it's a package. Don't recurse.
        if not is_package:
            for name, cls in _find_packages_in_module(name, module.__name__):
                loaded_packages[cls.name] = cls
    return loaded_packages


def _find_packages_in_module(module_name, parent_name):
    """Find all packages in the given module.

    :param str module_name: The module to inspect.
    :param str parent_name: The name of the package that this module is a
        child of.
    :yields tuple: A 2-tuple of (name, class).
    """
    imported = importlib.import_module("." + module_name, parent_name)
    for member in dir(imported):
        cls = getattr(imported, member)
        if is_package(cls):
            yield (member, cls)
