import typer
from datetime import datetime
from recap import catalogs
from recap.config import settings
from rich import print_json


app = typer.Typer(help="Read and search the data catalog.")


@app.command()
def search(
    query: str,
    time: datetime = typer.Option(
        None, '--as-of', '-a',
        help=\
            "View metadata as of a point in time.",
    ),
):
    """
    Searches the data catalog. The query string syntax is dependent on the data
    catalog.
    """

    with catalogs.create_catalog(**settings('catalog', {})) as c:
        results = c.search(query, time)
        print_json(data=results, sort_keys=True)


@app.command("list")
def list_(
    path: str = typer.Argument('/'),
    time: datetime = typer.Option(
        None, '--as-of', '-a',
        help=\
            "View metadata as of a point in time.",
    ),
):
    """
    Lists a data catalog directory's children.
    """

    with catalogs.create_catalog(**settings('catalog', {})) as c:
        results = sorted(c.ls(path, time) or [])
        print_json(data=results)


@app.command()
def read(
    path: str,
    time: datetime = typer.Option(
        None, '--as-of', '-a',
        help=\
            "View metadata as of a point in time.",
    ),
):
    """
    Prints metadata from a path in the data catalog.
    """

    with catalogs.create_catalog(**settings('catalog', {})) as c:
        results = c.read(path, time) or []
        print_json(data=results, sort_keys=True)