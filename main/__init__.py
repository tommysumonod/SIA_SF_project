import pymysql

# Force Django to use PyMySQL instead of mysqlclient
pymysql.version_info = (1, 4, 6, "final", 0)
pymysql.install_as_MySQLdb()