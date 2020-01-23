import smtplib
import jinja2
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

# from articles_list import articles

from credentials import credentials as credentials


def send_mail(
    username,
    password,
    to_whom="alinab8989@gmail.com",
    sender="bartosz.kobylinski@gmail.com",
    subject="New article has been published!",
    body=None,
):
    host = "smtp.gmail.com"
    port = 587
    massage = MIMEMultipart("alternative")
    massage["From"] = sender
    massage["Subject"] = subject
    massage["To"] = to_whom
    massage.attach(MIMEText(body, "html"))
    
    email_connection = smtplib.SMTP(host=host, port=port)
    email_connection.ehlo()
    email_connection.starttls()
    try:
        email_connection.login(username, password)
        email_connection.sendmail(sender, to_whom, massage.as_string())
    except Exception as error:
        print(error)
    finally:
        email_connection.quit()


def make_massage(articles):

    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    template = env.get_template("template.txt")
    massege = template.render(data=articles)
    return massege
