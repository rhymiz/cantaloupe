import os
import pathlib

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

TEMPLATE_DIR = os.path.join(pathlib.Path(__file__).parent, "templates")
template_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(),
)


def get_template_from_fs(template_name: str) -> Template:
    """
    Load template from filesystem by name

    :param template_name: name of template file
    :type template_name: str
    :return: Template object
    """
    return template_env.get_template(template_name)


def get_template_from_string(template: str) -> Template:
    """
    Directly create a template object

    :param template: template string
    :type template: str
    :return: Template object
    """
    return Template(template, autoescape=select_autoescape())
