import os
import pathlib
from functools import lru_cache

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

TEMPLATE_DIR = os.path.join(pathlib.Path(__file__).parent, "templates")
template_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(),
)


@lru_cache(maxsize=0)
def get_template(template_name: str) -> Template:
    return template_env.get_template(template_name)
