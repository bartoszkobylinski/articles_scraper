import requests



def shorten_link(link):
    data = {'url':link}
    a = requests.post(url='https://goolnk.com/api/v1/shorten', data=data)
    a = a.text
    return (a[15:-2])
