import pymysql
import django.db
pymysql.install_as_MySQLdb()
django.db.close_old_connections()
