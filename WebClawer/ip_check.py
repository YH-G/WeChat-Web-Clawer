import mysql
import threading
import requests
import ip_obtain


def ip_availability_test(ip_available, start, stop):
    print('Now checking' + str(ip_available[start:stop]))
    ip_available_temp = ip_available[start:stop]
    for ip in ip_available_temp:
        proxies = {
            "http": ip,
            "https": ip,
        }
        try:
            requests.get('https://www.google.com', timeout=2, proxies=proxies)
            print(ip + ' in the database is valid')
        except Exception as e:
            mysql.deletedb(ip)
            print(ip + ' is deleted from database')


def main():
    ip_available = mysql.inquerydb()

    if len(ip_available) == 0:
        ip_obtain.main()
    else:
        temp = int(len(ip_available) / 3)

        threads = []
        t1 = threading.Thread(target=ip_availability_test, args=(ip_available, 0, temp))
        threads.append(t1)
        t2 = threading.Thread(target=ip_availability_test, args=(ip_available, temp, 2 * temp))
        threads.append(t2)
        t3 = threading.Thread(target=ip_availability_test, args=(ip_available, 2 * temp, len(ip_available)))
        threads.append(t3)

        for t in threads:
            t.setDaemon(True)
            t.start()
        print('Now checking ip in the database')
        t.join()

    ip_available_new = mysql.inquerydb()

    print(str(len(ip_available_new)) + ' ip is valid in the database')

    if len(ip_available_new) < 10:
        print('IP in the database is not enough, now clawing new IP from the internet...')
        ip_obtain.main()


if __name__ == '__main__':
    main()
