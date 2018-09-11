from flask import Flask, render_template
import pymysql
import random

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def show_ip():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='ricot1993',
                         db='Webclawer')

    cursor = db.cursor()

    sql = 'SELECT IP FROM IP_list'

    ip_list = []

    try:
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        for i in results:
            ip_list.append(i[0])
        print(ip_list)
    except:
        db.rollback()

    random_num = random.randint(0, len(ip_list) - 1)
    ip = ip_list[random_num]

    return render_template('webpage.html', ip=ip)


if __name__ == '__main__':
    app.run()
