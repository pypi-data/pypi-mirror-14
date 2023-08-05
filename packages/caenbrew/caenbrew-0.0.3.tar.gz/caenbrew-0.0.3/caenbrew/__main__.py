# -*- coding: utf-8 -*-
import click

import caenbrew.packages

from . import get_config
from .packages import load_packages

_HELP_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
"""Click context settings to add '-h' as a help flag."""


@click.group(context_settings=_HELP_SETTINGS)
@click.option("--verbose", "-v",
              is_flag=True,
              help="Show all output")
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
        click.echo(_describe(value, "not found."))
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

    try:
        with package.prepare():
            package.download()
            package.install()
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
