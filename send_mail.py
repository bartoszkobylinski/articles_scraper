import logging
from jinja2 import Environment, FileSystemLoader, TemplateError


def make_message(article):
    try:
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template("template.txt")
        message = template.render(data=article)
    except TemplateError as template_err:
        logging.error(
            f"There was some template error during making a message: {template_err}")
    except Exception as error:
        logging.error(
            f"There was some unknown error during making a message: {error}")
    return message
