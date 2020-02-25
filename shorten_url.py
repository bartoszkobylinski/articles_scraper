import requests


def shorten_link(link):
    data = {"url": link}
    result = requests.post(url="https://goolnk.com/api/v1/shorten", data=data)
    short_link = result.text
    short_link = short_link[15:-2]
    short_link = short_link.replace('\\','')
    return short_link


