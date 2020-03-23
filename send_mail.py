import smtplib
import jinja2
import logging
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from jinja2 import Environment, FileSystemLoader
from email.message import EmailMessage


from credentials import credentials 


def make_message(article):
    try:
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template("template.txt")
        message = template.render(data=article)
    except Exception as error:
        logging.warning(f"Error occured while making a message: {error}")
    return message


def send_mail(article):
    msg = EmailMessage()
    msg['Subject'] = "Nowy artykul zostal opublikowany na wybranych portalach"
    msg['From'] = credentials['username']
    msg['To'] = credentials['to_whom']
    body = make_message(article)
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(credentials['username'], credentials['password'])
        smtp.send_message(msg)
