import sqlite3
import logging
import time
import smtplib
import requests
import requests_cache
import schedule

from selenium import webdriver

from current_ministry_of_finance import (
    get_current_articles_on_ministry_of_finance,
    get_current_articles_on_website_podatki_gov_pl,
)
from send_mail import send_mail, make_massage
from credentials import credentials as credentials
from shorten_url import shorten_link

username = credentials["username"]
password = credentials["password"]

logging.basicConfig(filename='financial_newsletter_log', level=logging.DEBUG)

to_smbdy = username
from_smbdy = username
subject = "Opublikowano wlasnie nowy artykul na obserwowanych portalach"

path = "/home/bart/PythonProjects/fin_min/chromedriver"
browser = webdriver.Chrome(executable_path=path)
browser.get("https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe?page=2")


def get_archive_article_from_archive():
    articles_list = []
    url_list = [
        "https://mf-arch2.mf.gov.pl/ministerstwo-finansow/wiadomosci/ostrzezenia-i-wyjasnienia-podatkowe",
        "https://mf-arch2.mf.gov.pl/web/bip/ministerstwo-finansow/wiadomosci/ostrzezenia-i-wyjasnienia-podatkowe?p_p_id=101_INSTANCE_M1vU&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_101_INSTANCE_M1vU_delta=20&_101_INSTANCE_M1vU_keywords=&_101_INSTANCE_M1vU_advancedSearch=false&_101_INSTANCE_M1vU_andOperator=true&cur=2",
    ]
    for url in url_list:
        browser.get(url)
        articles = browser.find_elements_by_class_name("article-source-title")
        for element in articles:
            article = {}
            article["title"] = element.text
            article["url"] = element.get_attribute("href")
            articles_list.append(article)
    logging.info('Articles from archive websites has been scraped. It has been found ' + str(len(articles_list)) +' articles')
    return articles_list


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
            logging.info("Article has been added to database")
            article["url"] = shorten_link(article["url"])
            send_mail(
                username, password, to_smbdy, from_smbdy, subject, make_massage(article)
            )
            database_connection.commit()


def get_archive_and_make_database():
    make_database()
    logging.info("I have made a database function")
    archive = get_archive_article_from_archive()
    logging.info('I have get archive variable')
    insert_articles_to_database(archive)
    logging.info("I have finished adding articles to database")


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

def job():
    get_archive_and_make_database()
    main_job_get_current_articles()

if __name__ == "__main__":

    schedule.every(5).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

