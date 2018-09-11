import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import urllib3
from pyquery import PyQuery as pq
import re
import MySQLdb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': '',
    'DNT': '1',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

ip_list_url = 'http://127.0.0.1:5000/'
ip_proxy = None


def get_ip():
    try:
        response = requests.get(ip_list_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError as e:
        return None


def get_html(url, count=1):
    print('Clawing', url)
    print('Trying count', count)
    global ip_proxy
    if count >= 5:
        print('Tried too many times')
        return None
    try:
        if ip_proxy:
            proxies = {
                "http": ip_proxy,
                "https": ip_proxy,
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)

        else:
            print('Now connecting web page without proxy')
            response = requests.get(url, allow_redirects=False, headers=headers)

        if response.status_code == 200:
            print('200, connected')
            return response.text
        elif response.status_code == 302:
            print('302, connection rejected')
            ip_proxy = get_ip()
            print(ip_proxy)
            if ip_proxy:
                print('Now using proxy ' + ip_proxy)
                return get_html(url)
            else:
                print('Getting Proxy Filed')
                return None
        else:
            print(response.status_code)
            ip_proxy = get_ip()
            return get_html(url)

    except Exception as e:
        print('An error occurred in getting html', e.args)
        count += 1
        ip_proxy = get_ip()
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    # print(html)
    links = doc('.news-box .news-list li .txt-box h3 a').items()
    for link in links:
        yield link.attr('href')


def get_detail(article_url):
    response = requests.get(article_url)
    if response.status_code == 200:
        # print(response.text)
        pattern_name = re.compile('var msg_title = "(.*?)"')
        pattern_date = re.compile('var publish_time = "(.*?)"')
        name = re.findall(pattern_name, response.text)[0]
        date = re.findall(pattern_date, response.text)[0]
        # print(name, date)
        return [name, date]


def create_table():
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         password='ricot1993',
                         db='Webclawer')
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS Wechat")

    sql = "CREATE TABLE Wechat (NAME CHAR(50), DATE CHAR(50),  URL CHAR(250), UNIQUE (NAME)) DEFAULT charset=utf8"

    cursor.execute(sql)
    db.close()


def insert_db(name, date, url):
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         password='ricot1993',
                         db='Webclawer',
                         charset='utf8')
    cursor = db.cursor()

    sql = 'INSERT INTO Wechat (NAME, DATE, URL) VALUES ("%s", "%s", "%s")' % (name, date, url)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


def main():
    create_table()
    for page in range(1, 10):
        print(page)
        html = get_index('风景', page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                print(article_url)
                article_details = get_detail(article_url)
                print(article_details)
                insert_db(article_details[0], article_details[1], article_url)


if __name__ == '__main__':
    main()
