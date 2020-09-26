import requests
import logging
from requests.exceptions import HTTPError, ConnectionError
from bs4 import BeautifulSoup


def get_current_articles_on_ministry_of_finance():

    url_ministry_of_finance_list = [
        "https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe",
        "https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe?page=2",
    ]
    articles_list = []
    for url in url_ministry_of_finance_list:
        response = requests.get(url)
        try:
            response.status_code == 200
        except ConnectionError as connection_error:
            logging.error(f"""While trying to get response from {url} an error occured: {connection_error}""")
        except Exception as error:
            logging.error(f"""While trying to get response from {url} an error occured: {error}""")

        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            articles = soup.find('div', class_='art-prev')
        except AttributeError as atr_error:
            logging.error(f"""While process scraper has not found articles insted an error occured: {atr_error}""")
        except Exception as error:
            logging.error(f"Another Exception has occured: {error}")

        titles = []
        links = []
        try:
            divs = articles.find_all('div', class_='title')
            for title in divs:
                titles.append(title.text)
        except AttributeError as atr_error:
            logging.error(f"""Erorr while finding divs in {url} has occured: {atr_error}""")
        except Exception as error:
            logging.error(f"""Erorr while finding divs in {url} has occured: {error}""")

        try:
            a_tags = articles.find_all('a', href=True)
            for url in a_tags:
                link = url['href']
                link = 'https://www.gov.pl' + link
                links.append(link)
        except Exception as error:
            logging.error(f"""Erorr while finding a_tag in {url} has occured: {error}""")

        for element in range(len(titles)):
            article = {}
            article["title"] = titles[element]
            article["url"] = links[element]
            articles_list.append(article)

    return articles_list


def get_current_articles_on_website_podatki_gov_pl():

    url_ministry_of_finance_list = [
        "https://www.podatki.gov.pl/cit/wyjasnienia/?page=1&query=",
        "https://www.podatki.gov.pl/cit/wyjasnienia/?page=2&query=",
        "https://www.podatki.gov.pl/pit/wyjasnienia-pit/?page=1&query=",
        "https://www.podatki.gov.pl/pit/wyjasnienia-pit/?page=2&query=",
        "https://www.podatki.gov.pl/pit/zmiany-w-prawie-pit/",
        "https://www.podatki.gov.pl/cit/zmiany-w-prawie-cit/",
        "https://www.podatki.gov.pl/vat/wyjasnienia/"
    ]
    articles_list = []
    for url in url_ministry_of_finance_list:
        response = requests.get(url)
        try:
            response.status_code == 200
        except HTTPError as http_err:
            logging.error(f"""Http Error: {http_err} has occured with response from url: {url}""")
        except Exception as error:
            logging.error(f"An error has occured: {error}")
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            divs = soup.find_all('div', class_='list-item')
        except Exception as error:
            logging.error(f"""Erorr while finding divs in podatki_gov has occured: {error}""")

        for div in divs:
            article = {}
            a_tag = div.find('a', href=True)
            article['title'] = a_tag.text[1:-1]
            link = "https://www.podatki.gov.pl" + a_tag['href']
            article['url'] = link
            articles_list.append(article)
    return articles_list


def get_current_articles_from_legislacja():

    url = "https://legislacja.gov.pl"
    try:
        response = requests.get(
            url,
            headers={
                'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
        response.raise_for_status()
    except HTTPError as error:
        logging.error(f'HTTP ERROR has ocured while scraping {url}: {error}')
    except Exception as error:
        logging.error(f"Another error has occured: {error}")
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        table = soup.find('table', class_='table-hover')
    except Exception as error:
        logging.error(f"Error has occured while scraping {url}: {error}")
    try:
        table_rows_list = table.find_all('tr')
        articles_list = []
        for row in table_rows_list:
            try:
                article = {}
                rowx = row.find('a', href=True)
                article['title'] = rowx.text
                article['url'] = 'https://legislacja.gov.pl' + rowx['href']
                articles_list.append(article)
            except Exception as error:
                logging.error(
                    f"""Error has occured while scraper try to find article in table on website {url}: {error}""")
    except Exception as error:
        logging.error(f"Error:{error}")
    finally:
        return articles_list


def get_current_articles_from_projects():
    url = 'https://www.sejm.gov.pl/Sejm9.nsf/agent.xsp?symbol=PROJNOWEUST&NrKadencji=9&Kol=D&Typ=UST'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        table = soup.find('table', class_='tab')
    except Exception as error:
        logging.error(f'Error: {error}')
    articles_list = []
    try:
        for tr in table.find_all('tr'):
            for a_tag in tr:
                article = {}
                try:
                    a_tag = tr.find('a', class_='pdf')
                except AttributeError as err:
                    logging.error(f'Error {err}')
                try:
                    anchor = a_tag['href']
                    title = a_tag.text
                    if a_tag['href'] == anchor and a_tag.text == title:
                        article['url'] = a_tag['href']
                        article['title'] = title
                        articles_list.append(article)
                        break
                except AttributeError as err:
                    logging.error(f'Error on url {url} as {err}')
                except TypeError as err:
                    logging.error(f'TypeError on url {url} as {err}')
    except Exception as error:
        logging.error(f"Error on url {url} as {error}")
    finally:
        return articles_list
