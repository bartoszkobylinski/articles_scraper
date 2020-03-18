import sqlite3
import logging
import time
import smtplib
import requests
import requests_cache
import schedule

from current_ministry_of_finance import (
    get_current_articles_on_ministry_of_finance,
    get_current_articles_on_website_podatki_gov_pl,
    get_current_articles_from_legislacja
)
from send_mail import send_mail, make_massage
from credentials import credentials as credentials
from shorten_url import shorten_link

username = credentials["username"]
password = credentials["password"]

logging.basicConfig(filename='financial_newsletter_log', level=logging.INFO)

to_smbdy = username
from_smbdy = username
subject = "Opublikowano wlasnie nowy artykul na obserwowanych portalach"


def make_database():
    database_connection = sqlite3.connect("articles.db")
    database_connection.execute("DROP TABLE IF EXISTS Articles")
    database_connection.commit()

    try:
        with database_connection:
            database_connection.execute(
                """CREATE TABLE Articles(
                Title TEXT,
                Link TEXT
            )"""
            )
    except sqlite3.OperationalError as error:
        logging.warning(error)
    logging.info("Database has been created.")


def insert_articles_to_database(articles_list):
    database_connection = sqlite3.connect("articles.db")
    cursor = database_connection.cursor()
    for article in articles_list:
        cursor.execute("SELECT Title from Articles WHERE Title=?", (article["title"],))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Articles VALUES (?,?)", (article["title"], article["url"])
            )
            print("Art has been added")
            logging.info("Article has been added to database")
            article["url"] = shorten_link(article["url"])
            try:
                send_mail(
                    username, password, to_smbdy, from_smbdy, subject, make_massage(article)
                )
                print("I have send mail")
            except Exception as error:
                print(error)
            database_connection.commit()


def get_archive_and_make_database():
    make_database()
    logging.info("I have made a database function")


def main_job_get_current_articles():
    logging.info("I'm starting get current articles")
    articles = get_current_articles_on_ministry_of_finance()
    logging.info("I have finished getting articles from ministry of finance")
    insert_articles_to_database(articles)
    logging.info(
        """
        Gathered articles are inserted in to database 
        and now I'm starting gathering current articles from podatki.gov.pl"""
        )
    articles = get_current_articles_on_website_podatki_gov_pl()
    logging.info("I have finished getting articles from podatki.gov.pl")
    insert_articles_to_database(articles)
    articles = get_current_articles_from_legislacja()
    logging.info("I have finished getting articles from legislacja")
    insert_articles_to_database(articles)

def job():
    print("I have started scraping")
    main_job_get_current_articles()

if __name__ == "__main__":

    #get_archive_and_make_database()
    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

