import requests
import logging
from requests import Response
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
            #make a logging system
        except Exception as error:
            logging.info("Error has occured: " + str(error))
    
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find('div',class_='art-prev')
        divs = articles.find_all('div', class_='title')
        titles = []
        for title in divs:
            titles.append(title.text)

        a_tags = articles.find_all('a', href = True)
        links = []
        for url in a_tags:
            link = url['href']
            link = 'https://www.gov.pl' + link
            links.append(link)
        
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
            #make a logging system
        except Exception as error:
            logging.info("Error has occured: " + str(error))
    
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='list-item')
        
        for div in divs:
            article = {}
            a_tag = div.find('a', href= True)
            article['title'] = a_tag.text[1:-1]
            link = "https://www.podatki.gov.pl" + a_tag['href']
            article['url'] = link
            articles_list.append(article)
    return articles_list
def get_current_articles_from_legislacja():
    
    url = "https://legislacja.gov.pl"
    try:
        response = requests.get(url, 
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})
    except Exception as error:
        logging.info("Error has occured: " + str(error))

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        table = soup.find('table', class_='table')
    except Exception as error:
        logging.info("Error has occured: " + str(error))
    table_rows_list = table.find_all('tr')
    articles_list = []
    for row in table_rows_list:
        try:
            article = {}
            rowx = row.find('a', href=True)
            article['title'] = rowx.text
            article['url'] = 'https://legislacja.gov.pl' + rowx['href']
            articles_list.append(article)
        except Exception as er:
            logging.info("Error has occured: " + str(er))
    
    return articles_list


