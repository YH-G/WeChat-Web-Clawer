import MySQLdb


def creattable():
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         password='ricot1993',
                         db='Webclawer')
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS IP_list")

    sql = "CREATE TABLE IP_list (TIME CHAR(100), IP CHAR(100), UNIQUE (IP))"

    cursor.execute(sql)
    db.close()


def insertdb(time, ip):
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         password='ricot1993',
                         db='Webclawer')
    cursor = db.cursor()

    sql = 'INSERT INTO IP_list(TIME, IP) VALUES ("%s", "%s")' % (time, ip)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()


def inquerydb():
    db = MySQLdb.connect(host='localhost',
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
        # print(ip_list)
        return ip_list
    except:
        db.rollback()

    db.close()


def deletedb(ip):
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         password='ricot1993',
                         db='Webclawer')
    cursor = db.cursor()

    sql = 'DELETE FROM IP_list WHERE IP = "%s"' % ip

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()

# inquerydb()
# creattable()
