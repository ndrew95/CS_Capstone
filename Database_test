import pymysql
import pymysql.cursors

host='cap-comp.cpwue0appyn7.us-west-2.rds.amazonaws.com'
port=3306
dbname= 'Companion'
user="admin234"
password="tf7A8sjX#!"

conn = pymysql.connect(db=dbname,host=host, password=password, port=port, user=user)
cursor = conn.cursor()

#cursor.execute("CREATE TABLE test (name VARCHAR(255), address VARCHAR(255))")
cursor.execute("SHOW TABLES")

for x in cursor:
	print(x)
cursor.close()
