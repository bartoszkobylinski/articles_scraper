import logging
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPException, SMTPServerDisconnected
from jinja2 import Environment, FileSystemLoader, TemplateError
from credentials import credentials


def make_message(article):
    try:
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template("template.txt")
        message = template.render(data=article)
    except TemplateError as template_err:
        logging.error(f"There was some template error during making a message: {template_err}")
    except Exception as error:
        logging.error(f"There was some unknown error during making a message: {error}")
    return message


def send_mail(article):
    msg = EmailMessage()
    msg['Subject'] = "Nowy artykul zostal opublikowany na wybranych portalach"
    msg['From'] = os.environ.get('ARTICLES_SCRAPER_GMAIL_USERNAME')
    msg['To'] = credentials['to_whom']
    body = make_message(article)
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        logging.debug(f"{smtp.set_debuglevel(1)}")
        try:
            smtp.login(os.environ.get('ARTICLES_SCRAPER_GMAIL_USERNAME'),
                       os.environ.get('ARTICLES_SCRAPER_PASSWORD'))
        except SMTPServerDisconnected as smtp_serv_disc:
            logging.error(
                f"There was some problem with smtp connection because SMTPServerDisconnected: {smtp_serv_disc}")
        except SMTPConnectError as smtp_conn_err:
            logging.error(
                f"There were some problems with smtp connection because SMTPConnectError occured: {smtp_conn_err}")
        except SMTPAuthenticationError as smtp_auth_err:
            logging.error(
                f"There was some problem with authentication: {smtp_auth_err}")
        except SMTPException as smtp_except:
            logging.error(f"there was some smtp problem: {smtp_except}")
        except Exception as error:
            logging.error(f"there was some unknown exception: {error}")
        try:
            smtp.send_message(msg)
            now = datetime.now()
            logging.info(f'The mail has been sent at: {now.strftime("%m:%d:%H:%M:%S")}')
        except Exception as error:
            now = datetime.now()
            logging.error(f"""Error has occured while script tried to send
            message from your mail account at {now.strftime("%m:%d:%H:%M:%S")} and the error is: {error}""")
