import datetime
import logging
import sqlite3
import time

import schedule

from current_ministry_of_finance import (
    get_current_articles_from_legislacja, get_current_articles_from_projects,
    get_current_articles_on_ministry_of_finance,
    get_current_articles_on_website_podatki_gov_pl)
from send_mail import send_mail
from shorten_url import shorten_link

logging.basicConfig(filename='financial_newsletter_log', level=logging.INFO)


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
        cursor.execute("SELECT Title from Articles WHERE Title=?",
                       (article["title"],))
        result = cursor.fetchone()
        if not result:
            cursor.execute(
                "INSERT INTO Articles VALUES (?,?)", (article["title"],
                                                      article["url"]))
            logging.info("Article has been added to database")
            article["url"] = shorten_link(article["url"])
            time.sleep(30)
            send_mail(article)
            current_time = datetime.datetime.now()
            current_time = current_time.strftime("%b %d %Y %H:%M")
            logging.info(f"Mail has been send at {current_time}.")
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
    logging.info(
        """
        Gathered articles are inserted in to database
        and now I'm starting gathering current articles from legislacja"""
        )
    articles = get_current_articles_from_legislacja()
    logging.info("I have finished getting articles from legislacja")
    insert_articles_to_database(articles)
    logging.info(
        """
        Gathered articles are inserted in to database
        and now I'm starting gathering current articles from projects"""
        )
    articles = get_current_articles_from_projects()
    logging.info("I have finished getting articles from projects")
    insert_articles_to_database(articles)


def job():
    print("I have started scraping")
    main_job_get_current_articles()


if __name__ == "__main__":
    # get_archive_and_make_database()
    main_job_get_current_articles()
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
