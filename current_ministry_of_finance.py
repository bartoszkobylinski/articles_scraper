from selenium import webdriver
import time


path = "/home/bart/PythonProjects/flight/chrome/chromedriver"
browser = webdriver.Chrome(path)


def get_current_articles_on_ministry_of_finance():
    url_ministry_of_finance_list = [
        "https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe",
        "https://www.gov.pl/web/finanse/ostrzezenia-i-wyjasnienia-podatkowe?page=2",
    ]

    title_list = []
    url_list = []
    articles_list = []
    for url in url_ministry_of_finance_list:
        browser.get(url)
        articles = browser.find_element_by_class_name("art-prev--near-menu")
        articles_title = articles.find_elements_by_tag_name("li")
        for article in articles_title:
            titles = article.find_elements_by_class_name("title")
            for title in titles:
                title_list.append(title.text)
        article_urls = articles.find_elements_by_tag_name("a")
        for article_url in article_urls:
            url_list.append(article_url.get_attribute("href"))
    for element in range(len(title_list)):
        article = {}
        article["title"] = title_list[element]
        article["url"] = url_list[element]
        articles_list.append(article)

    return articles_list


def get_current_articles_on_website_podatki_gov_pl():
    articles_list = []
    url_podatki_gov_pl_list = [
        "https://www.podatki.gov.pl/cit/wyjasnienia/?page=1&query=",
        "https://www.podatki.gov.pl/cit/wyjasnienia/?page=2&query=",
        "https://www.podatki.gov.pl/pit/wyjasnienia-pit/?page=1&query=",
        "https://www.podatki.gov.pl/pit/wyjasnienia-pit/?page=2&query=",
        "https://www.podatki.gov.pl/pit/zmiany-w-prawie-pit/",
        "https://www.podatki.gov.pl/cit/zmiany-w-prawie-cit/",
        "https://www.podatki.gov.pl/vat/wyjasnienia/",
    ]
    for url in url_podatki_gov_pl_list:
        browser.get(url)
        articles = browser.find_element_by_class_name("col-md-9")
        articles_title = articles.find_elements_by_class_name("list-item")
        for anchor in articles_title:
            anchor_tag = anchor.find_element_by_tag_name("a")
            header_2 = anchor_tag.find_element_by_tag_name("h2")
            article = {}
            article["title"] = header_2.text
            article["url"] = anchor_tag.get_attribute("href")
            articles_list.append(article)
    return articles_list
