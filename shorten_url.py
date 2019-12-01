import requests



def shorten_link(link):
    data = {'url':link}
    a = requests.post(url='https://goolnk.com/api/v1/shorten', data=data)
    a = a.text
    return (a[15:-2])

a = shorten_link('https://upload.wikimedia.org/wikipedia/commons/9/99/InsSight_spacecraft_appendix_gallery_Image_55-full.jpg')
print(a)