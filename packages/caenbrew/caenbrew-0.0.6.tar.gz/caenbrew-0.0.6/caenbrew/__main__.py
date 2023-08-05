# -*- coding: utf-8 -*-
import click

import caenbrew.packages

from . import get_config
from .packages import load_packages
from .packaging import calculate_dependencies

_HELP_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
"""Click context settings to add '-h' as a help flag."""


@click.group(context_settings=_HELP_SETTINGS)
@click.option("--verbose", "-v",
              is_flag=True,
              help="Show all output")
@click.version_option()
@click.pass_context
def cli(ctx, verbose):
    """caenbrew -- install packages on CAEN."""
    config = get_config()

    # If the user explicitly sets verbose on the command-line, override the
    # configuration value.
    if verbose:
        config["verbose"] = True
    elif "verbose" not in config:
        config["verbose"] = False

    packages = load_packages(caenbrew.packages)
    packages = {i: j(config) for i, j in packages.iteritems()}

    ctx.obj = {
        "config": config,
        "packages": packages,
    }


def _lookup_package(ctx, param, value):
    """Convert a package name into an actual package."""
    try:
        return ctx.obj["packages"][value]
    except KeyError:
        _fail(_describe(value, "not found."))
        ctx.exit(1)


@cli.command(context_settings=_HELP_SETTINGS)
@click.argument("package", callback=_lookup_package)
@click.option("--force", "-f", is_flag=True, help="Force (re)installation.")
@click.pass_context
def install(ctx, package, force):
    """Install a package."""
    if package.is_installed:
        if force:
            click.echo(_describe(package, "already installed, "
                                          "but continuing anyways."))
        else:
            _succeed(_describe(package, "already installed."))
            return

    dependencies = calculate_dependencies(type(package))
    click.echo("Packages to install: {}"
               .format(_package_names(dependencies)))

    try:
        for i in dependencies:
            dep = ctx.obj["packages"][i.name]
            if dep.is_installed and not force:
                _succeed(_describe(dep, "already installed."))
            else:
                click.echo(_describe(dep, "starting installation..."))
                with dep.prepare():
                    dep.download()
                    dep.install()
    except Exception as e:
        _fail(_describe(
            package,
            "installation failed: {}"
            .format(click.style(str(e), bold=True, fg="red"))
        ))
        if not str(e) or ctx.obj["config"]["verbose"]:
            raise
    except KeyboardInterrupt:
        _fail("Cancelled.")
    else:
        _succeed(_describe(package, "installed."))


@cli.command(context_settings=_HELP_SETTINGS)
@click.argument("package", callback=_lookup_package)
@click.pass_context
def uninstall(ctx, package):
    """Uninstall a package."""
    if not package.is_installed:
        _fail(_describe(package, "not installed."))
        return

    try:
        package.uninstall()
    except Exception as e:
        _fail(_describe(
            package,
            "uninstallation failed: {}"
            .format(click.style(e.message, bold=True, fg="red"))
        ))
        if not str(e) or ctx.obj["config"]["verbose"]:
            raise
    except KeyboardInterrupt:
        _fail("Cancelled.")
    else:
        _succeed(_describe(package, "uninstalled."))


@cli.command(context_settings=_HELP_SETTINGS)
@click.argument("package", callback=_lookup_package)
def info(package):
    """Show information about a package."""
    info = package.__doc__
    if info:
        click.echo(info)
    else:
        _fail(_describe(package, "has no documentation."))

    click.echo()
    click.echo("Homepage: {}".format(package.homepage))
    click.echo("Version: {}".format(package.version))

    if package.dependencies:
        click.echo("Dependencies: {}"
                   .format(_package_names(package.dependencies)))
    else:
        click.echo("Dependencies: none")

    if package.is_installed:
        _succeed(_describe(package, "is installed."))
    else:
        _fail(_describe(package, "is not installed."))


def _succeed(message):
    u"""Print a success message.

    Looks like this:

        ✓ Something happened!

    :param str message: The success message to print.
    """
    click.echo("{} {}".format(click.style("✓", fg="green"),
                              message))


def _fail(message):
    u"""Print a failure message.

    Looks like this:

        ✗ Something happened!

    :param str message: The failure message to print.
    """
    click.echo("{} {}".format(click.style("✗", fg="red"),
                              message))


def _describe(package, message):
    """Describe a package with the given message.

    Given package = VimPackage, message = "already installed", this would
    return:

        Package vim already installed

    But "vim" would be bolded.

    :param BasePackage|str package: The package or the package name.
    :param str message: The message about the package.
    :returns str: The formatted string with a bolded package name.
    """
    try:
        package_name = package.name
    except AttributeError:
        package_name = package

    return "Package {} {}".format(click.style(package_name, bold=True),
                                  message)


def _package_names(packages):
    """Bold each package name in a comma-separated list of package names.

    :param list packages: The list of packages.
    :returns str: A comma-separated list of bolded package names.
    """
    return ", ".join(click.style(i.name, bold=True)
                     for i in packages)
