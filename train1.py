from bs4 import BeautifulSoup
import urllib.request as req


def get_html():
    url = 'http://www.aozora.gr.jp/'
    res = req.urlopen(url)
    try:
        soup = BeautifulSoup(res, 'html.parser')
    except:
        print('ぱーすできませーん')
    title = soup.find('h1').string
    print(title)


if __name__ == '__main__':
    get_html()
