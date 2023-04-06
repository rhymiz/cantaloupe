from __future__ import annotations

import click

from .commands.init import init
from .commands.make_code import make_code


@click.group()
def entry() -> None:
    pass


entry.add_command(make_code)
entry.add_command(init)
