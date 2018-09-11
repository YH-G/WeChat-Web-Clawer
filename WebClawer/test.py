import mysql, time

cur_time = time.strftime('%Y-%m-%d %X', time.localtime())
print(cur_time)
mysql.insertdb(cur_time, '123456')
