from playhouse.pool import PooledMySQLDatabase  # mysql连接池
from playhouse.shortcuts import ReconnectMixin  # mysql连接中断重连


class ReconnectMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    # python的mro 研究
    ...


MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_DATABASE = "mxshop_user_srv"
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345678"

DB = ReconnectMySQLDatabase(MYSQL_DATABASE, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
