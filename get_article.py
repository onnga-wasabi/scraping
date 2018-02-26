from bs4 import BeautifulSoup
import urllib.request as req
import sqlite3
import re

dbname = 'gigazin.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
table_name = 'security'


def get_urls(category_url):
    res = req.urlopen(category_url)
    try:
        soup = BeautifulSoup(res, 'lxml')
    except:
        soup = BeautifulSoup(res, 'html5lib')
    cards = soup.find_all('div', class_='card')
    titles = [str(card.h2.a.span.string) for card in cards]
    atags = [card.h2.a.unwrap() for card in cards]
    urls = [re.sub('<a href="', '', re.sub('\"></a>', '', str(atag)))
            for atag in atags]
    return titles, urls


def get_html(urli, tag='p', class_='preface'):
    res = req.urlopen(url)
    try:
        soup = BeautifulSoup(res, 'lxml')
    except:
        soup = BeautifulSoup(res, 'html5lib')
    title = soup.find('h1').string
    p_list = soup.find_all(tag, class_=class_)
    p_list = [re.sub('<(\'.*?\'|\".*?\"|[^\'\"])*?>', '', str(p))
              for p in p_list]
    return (title, str(p_list))


def create_table(table_name):
    sql = 'create table if not exists {} (title varchar(64),p_list varchar(32))'.format(
        table_name)
    c.execute(sql)


def insert_data(table_name, data):
    sql = 'insert into {} (title,p_list) values (?,?)'.format(table_name)
    c.executemany(sql, (data,))
    conn.commit()


def drop_table(table_name):
    sql = 'drop table if exists {}'.format(table_name)
    c.execute(sql)


def update(table_name, url):
    test = get_html(url)
    insert_data(table_name, test)


if __name__ == '__main__':
    drop_table(table_name)
    create_table(table_name)
    security = 'https://gigazine.net/news/C14/'
    titles, urls = get_urls(security)
    '''
    for url in zip(titles, urls):
        update(table_name, url)
    sql = 'select * from {}'.format(table_name)
    for row in c.execute(sql):
        print(row)
    '''
    conn.close()
