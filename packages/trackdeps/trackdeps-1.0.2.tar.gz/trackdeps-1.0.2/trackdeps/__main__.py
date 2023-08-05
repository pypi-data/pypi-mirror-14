"""
    trackdeps.__main__
    CLI entry point for trackdeps

    Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
    Released under the MIT license
"""

import click

from . import report


@click.command()
@click.argument("config")
@click.option("-o", "--output", help="Set the output directory",
              default="-")
@click.option("-f", "--force", help="Override existing output file",
              is_flag=True)
def cli(config, output, force):
    """Generate a report from the config file"""
    try:
        report.generate(config, output, force)
    except report.GenerationError as e:
        print("Error: %s" % e)


if __name__ == "__main__":
    cli()
