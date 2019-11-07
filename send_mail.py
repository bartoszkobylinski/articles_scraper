from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

from articles_list import articles

from credentials import credentials


def send_mail(to_whom, sender, subject, body, credentials):
    host = "smtp.gmail.com"
    port = 587
    username = credentials['username']
    password = credentials['password']
    #-------------------------------------
    massage = MIMEMultipart('alternative')
    massage['From'] = sender
    massage['Subject'] = subject
    massage['To'] = to_whom
    massage.attach(MIMEText(body, 'html'))
    #------------------------------------------
    email_connection = smtplib.SMTP(host=host,port=port)
    email_connection.ehlo()
    email_connection.starttls()
    try:
        email_connection.login(username,password)
        email_connection.sendmail(sender,to_whom,massage.as_string())
    except Exception as e:
        print(e)
    finally:
        email_connection.quit()


to_whom = 'alinab8989@gmail.com'
'''


from_email = username
send_to_list = ['alinab8989@gmail.com']

email_connection = smtplib.SMTP(host=host,port=port)
email_connection.ehlo()
email_connection.starttls()
try:
    email_connection.login(username,password)
    email_connection.sendmail(from_email,send_to_list,"Hi, I LOEEEEOEVEEEE YOUUUUUU")
except SMTPAuthenticationError:
    print('error')
email_connection.quit()
'''

def make_massage(articles):

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('template.txt')
    massege = template.render(data=articles)
    return massege

a = make_massage(articles)
print(a)
