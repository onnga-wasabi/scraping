from bs4 import BeautifulSoup
import urllib.request as req
import sqlite3
import re
import datetime

dbname = 'gigazin.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()
table_name = 'top'


def get_urls(category_url, today):
    '''
    gigazinのトップの記事から今日の日付で投稿された記事のtitleとurlを取得
    '''
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
    dtags = [card.time.unwrap() for card in cards]
    days = [re.sub('<.*\"', '', re.sub('T.*>', '', str(dtag)))
            for dtag in dtags]
    for idx, day in enumerate(days):
        if not day == today:
            break
    return titles[:idx], urls[:idx]


def get_html(url, tag='p', class_='preface'):
    '''
    渡されたurlから指定のタグの中身を抜き出す
    正規表現でパースしてるところは単にタグを外してるだけ
    '''
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
    '''
    渡されたテーブル名が存在しなければ作成
    '''
    sql = 'create table if not exists {} (title varchar(64),article varchar,date int,url varchar(1024))'.format(
        table_name)
    c.execute(sql)


def insert_data(table_name, data):
    '''
    タイトル，記事，日付，urlを挿入
    '''
    sql = 'insert into {} (title,article,date,url) values (?,?,?,?)'.format(
        table_name)
    c.executemany(sql, (data,))
    conn.commit()


def drop_table(table_name):
    '''
    tableを削除
    '''
    sql = 'drop table if exists {}'.format(table_name)
    c.execute(sql)


def update(table_name, url, today):
    '''
    get_htmlで得たデータに日付をプラスしてデータベースに追加
    '''
    title, article = get_html(url)
    data = (title, article, int(today), url)
    insert_data(table_name, data)


def main():
    '''
    gigazinのトップから全ての記事にたいして記事を取得し保存
    '''
    create_table(table_name)
    top = 'https://gigazine.net/'
    today = datetime.date.today()
    titles, urls = get_urls(top, str(today))
    today = re.sub('-', '', str(today))

    sql = 'select title from {} where date = ?'.format(table_name)
    pre_titles = [title[0] for title in c.execute(sql, (today,))]

    for title, url in zip(titles, urls):
        if title in pre_titles:
            print('ほぞんちゅう：', title)
            continue
        update(table_name, url, today)
    conn.close()
    return 0


if __name__ == '__main__':
    # drop_table(table_name)
    main()
