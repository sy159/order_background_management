import pymysql
from django.db import connections

pymysql.install_as_MySQLdb()


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()
