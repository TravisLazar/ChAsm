"""
Chasm CLI - Command Line Interface for Chart Assembler
"""

import click
from chasm.library.chart import make_chart
from chasm.library.data import parse_data_input
from typing import List
from . import __version__


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)


@main.command()
def info():
    click.echo(f"Chasm v{__version__}")
    click.echo("Chart Assembler - a simple workflow for creating charts")


@main.command()
@click.argument('chart_type', type=click.Choice(['bar', 'stackedbar']))
@click.option('--data', '-d', help='raw data, as a list of dicts')
@click.option('--layer', '-l', multiple=True, help='list of paths to layer files, processed in order')
@click.option('--mod', '-m', multiple=True, help='list of paths to manipulator files, processed in order')
@click.option('--output-path', '-o', default='build/chart.svg', help='path to output graphic')
def make(chart_type: str, data: str, layer: List[str], mod: List[str], output_path: str):
    make_chart(chart_type, raw_data=data, layer_paths=layer, mod_paths=mod, output_path=output_path)


@main.command()
@click.option('--data', '-d', help='raw data, as a list of dicts')
@click.option('--mod', '-m', multiple=True, help='list of paths to manipulator files, processed in order')
def data(data: str, mod: List[str]):
    click.echo(f"Data: {data}")
    click.echo(f"Mods: {mod}")
    data = parse_data_input(data, mod)
    print(data)



if __name__ == "__main__":
    main()