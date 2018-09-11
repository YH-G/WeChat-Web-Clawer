import requests
from bs4 import BeautifulSoup
import multiprocessing
import time
import mysql
import threading
import queue

q = queue.Queue()


def ip_html_obtain():
    url = 'https://free-proxy-list.net/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException:
        print('An error occurred when accessing the internet')
        return None


def ip_obtain(page_html):
    soup = BeautifulSoup(page_html, 'lxml')
    ip_list = soup.find_all('tbody')[0].find_all('tr')
    ip_obtained_list = []
    for ip_content in ip_list:
        ip_temp = ip_content.find_all('td')
        ip = "http://" + ip_temp[0].getText() + ":" + ip_temp[1].getText()
        ip_obtained_list.append(ip)
    print(str(len(ip_obtained_list)) + ' new ip obtained')
    return ip_obtained_list


def ip_availability_test(ip_obtained, start, stop):
    print('Now checking the availability of new ip...')
    ip_obtained_temp = ip_obtained[start:stop]
    # print(ip_obtained_temp)
    for ip in ip_obtained_temp:
        proxies = {
            "http": ip,
            "https": ip,
        }
        try:
            response = requests.get('https://www.google.com', timeout=2, proxies=proxies)
            if response.status_code == 200:
                q.put(ip)
        except Exception as e:
            print(ip + ' is not available')


def main():
    page_html = ip_html_obtain()
    ip_obtained = ip_obtain(page_html)
    temp = int(len(ip_obtained) / 5)

    threads = []
    t1 = threading.Thread(target=ip_availability_test, args=(ip_obtained, 0, temp))
    threads.append(t1)
    t2 = threading.Thread(target=ip_availability_test, args=(ip_obtained, temp, 2 * temp))
    threads.append(t2)
    t3 = threading.Thread(target=ip_availability_test, args=(ip_obtained, 2 * temp, 3 * temp))
    threads.append(t3)
    t4 = threading.Thread(target=ip_availability_test, args=(ip_obtained, 3 * temp, 4 * temp))
    threads.append(t4)
    t5 = threading.Thread(target=ip_availability_test, args=(ip_obtained, 4 * temp, len(ip_obtained)))
    threads.append(t5)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    ip_id = 0
    while not q.empty():
        ip_id += 1
        cur_time = time.strftime('%Y-%m-%d %X', time.localtime())

        mysql.insertdb(cur_time, q.get())

    print(str(ip_id) + ' new ip added to the database')


if __name__ == '__main__':
    main()
