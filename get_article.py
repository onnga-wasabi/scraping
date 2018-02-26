from bs4 import BeautifulSoup
import urllib.request as req
import sqlite3
import re
import datetime

dbname = 'gigazin.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
table_name = 'top'


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


def get_html(url, tag='p', class_='preface'):
    res = req.urlopen(url)
    try:
        soup = BeautifulSoup(res, 'lxml')
    except:
        soup = BeautifulSoup(res, 'html5lib')
    title = soup.find('h1').string
    p_list = soup.find_all(tag, class_=class_)
    p_list = [re.sub('<(\'.*?\'|\".*?\"|[^\'\"])*?>', '', str(p))
              for p in p_list]
    return (title, str(''.join(p_list)))


def create_table(table_name):
    sql = 'create table if not exists {} (title varchar(64),article varchar,date int)'.format(
        table_name)
    c.execute(sql)


def insert_data(table_name, data):
    sql = 'insert into {} (title,article,date) values (?,?,?)'.format(
        table_name)
    c.executemany(sql, (data,))
    conn.commit()


def drop_table(table_name):
    sql = 'drop table if exists {}'.format(table_name)
    c.execute(sql)


def update(table_name, url, today):
    title, article = get_html(url)
    data = (title, article, int(today))
    insert_data(table_name, data)


def main():
    # drop_table(table_name)
    create_table(table_name)
    top = 'https://gigazine.net/'
    titles, urls = get_urls(top)
    sql = 'select title from {} '.format(table_name)
    pre_titles = [title[0] for title in c.execute(sql)]
    today = datetime.date.today()
    today = re.sub('-', '', str(today))
    for title, url in zip(titles, urls):
        if title in pre_titles:
            print(title)
            continue
        update(table_name, url, today)
    conn.close()
    return 0


if __name__ == '__main__':
    main()
