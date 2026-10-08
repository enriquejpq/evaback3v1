import pymysql
pymysql.install_as_MySQLdb()

import django.db.backends.mysql.base
django.db.backends.mysql.base.Database.version_info = (11, 0, 0, 'final', 0)


