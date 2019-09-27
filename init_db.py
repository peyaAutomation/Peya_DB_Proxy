from peewee import MySQLDatabase

from libs.Utils import Utils
from models.models import QueryEntity

db = MySQLDatabase(
            Utils.get_env_var('MY_SQL_DATABASE_QUERY_REPO'),
            **{
                'charset': 'utf8',
                'use_unicode': True,
                'host': Utils.get_env_var('MY_SQL_HOST_QUERY_REPO'),
                'port': int(Utils.get_env_var('MY_SQL_PORT_QUERY_REPO')),
                'user': Utils.get_env_var('MY_SQL_USER_QUERY_REPO'),
                'password': Utils.get_env_var('MY_SQL_PASS_QUERY_REPO')
            }
        )

tables = [
    QueryEntity
]

db.drop_tables(tables)
db.create_tables(tables)
