"""
Chasm CLI - Command Line Interface for Chart Assembler
"""

import click
from chasm.library.chart import make_chart
from . import __version__


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


@main.command()
def info():
    click.echo(f"Chasm v{__version__}")
    click.echo("Chart Assembler - A tool for creating charts from data")


@main.command()
@click.option('--data', '-d', help='raw data, as a list of dicts')
@click.option('--layer', '-l', multiple=True, help='list of paths to layer files, processed in order')
def bar(data, layer):
    make_chart("bar", raw_data=data, layer_paths=layer, output_folder="build")


if __name__ == "__main__":
    main()