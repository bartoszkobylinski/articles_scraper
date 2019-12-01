import sqlite3
import logging
import time
import smtplib
import requests
import requests_cache
import schedule

from selenium import webdriver

from current_ministry_of_finance import get_current_articles_on_ministry_of_finance, get_current_articles_on_website_podatki_gov_pl
from send_mail import send_mail, make_massage
from credentials import credentials as credentials
from shorten_url import shorten_link

username = credentials['username']
password = credentials['password']

to_smbdy = 'bartosz.kobylinski@gmail.com'
from_smbdy = 'bartosz.kobylinski@gmail.com'
subject = "Opublikowano wlasnie nowy artykul na obserwowanych portalach"

path = "/home/bart/PythonProjects/flight/chrome/chromedriver"
browser = webdriver.Chrome(path)
browser.get('https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe?page=2')

def get_archive_article_from_archive():
    articles_list = []
    url_list = ['https://mf-arch2.mf.gov.pl/ministerstwo-finansow/wiadomosci/ostrzezenia-i-wyjasnienia-podatkowe',
    'https://mf-arch2.mf.gov.pl/web/bip/ministerstwo-finansow/wiadomosci/ostrzezenia-i-wyjasnienia-podatkowe?p_p_id=101_INSTANCE_M1vU&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_101_INSTANCE_M1vU_delta=20&_101_INSTANCE_M1vU_keywords=&_101_INSTANCE_M1vU_advancedSearch=false&_101_INSTANCE_M1vU_andOperator=true&cur=2'
    ]
    for url in url_list:
        browser.get(url)
        articles = browser.find_elements_by_class_name('article-source-title')
        for element in articles:
            article = {}
            article['title'] = element.text
            article['url'] = element.get_attribute('href')
            articles_list.append(article)
    return articles_list


def make_database():
    database_connection = sqlite3.connect('articles.db')
    database_connection.execute("DROP TABLE IF EXISTS Articles")
    database_connection.commit()

    try:
        with database_connection:
            database_connection.execute("""CREATE TABLE Articles(
                Title TEXT,
                Link TEXT
            )""")
    except sqlite3.OperationalError as error:
        logging.warning(error)

def insert_articles_to_database(articles_list):
    database_connection = sqlite3.connect('articles.db')
    cursor = database_connection.cursor()
    for article in articles_list:
        cursor.execute("SELECT Title from Articles WHERE Title=?",(article['title'],))
        result = cursor.fetchone()
        if not result:
            cursor.execute("INSERT INTO Articles VALUES (?,?)",(article['title'],article['url']))
            article['url'] = shorten_link(article['url'])
            send_mail(username,password, to_smbdy, from_smbdy, subject, make_massage(article))
            database_connection.commit()

def get_archive_and_make_database():
    make_database()
<<<<<<< HEAD
    a = get_archive_article_from_archive()
    insert_articles_to_database(a)
    a = get_current_articles_on_ministry_of_finance()
    insert_articles_to_database(a)
    a = get_current_articles_on_website_podatki_gov_pl()
    insert_articles_to_database(a)
main()
print("It's done!")
=======
    archive = get_archive_article_from_archive()
    insert_articles_to_database(archive)
def main_job_get_current_articles():
    articles = get_current_articles_on_ministry_of_finance()
    insert_articles_to_database(articles)
    articles = get_current_articles_on_website_podatki_gov_pl()
    insert_articles_to_database(articles)

if __name__ == "__main__":
    
    get_archive_and_make_database()
    schedule.every().day.at("08:00").do(main_job_get_current_articles)

    while True:
        schedule.run_pending()
        time.sleep(1)
>>>>>>> 0c327c26a7927ae53c01680c93486696770e91d7
