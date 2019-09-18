import pymysql
from django.db import connections

pymysql.install_as_MySQLdb()


def close_old_connections(**kwargs):
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()

signals.request_started.connect(close_old_connections)
signals.request_finished.connect(close_old_connections)
