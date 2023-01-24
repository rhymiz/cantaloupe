import os
import pathlib

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

TEMPLATE_DIR = os.path.join(pathlib.Path(__file__).parent, "templates")
template_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(),
)


def get_template_from_fs(template_name: str) -> Template:
    """load template from filesystem by name"""
    return template_env.get_template(template_name)


def get_template_from_string(template: str) -> Template:
    """directly create a template object"""
    return Template(template, autoescape=select_autoescape())
