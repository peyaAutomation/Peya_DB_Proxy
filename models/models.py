from peewee import *
from libs.Utils import Utils


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):

    class Meta:
        database = MySQLDatabase(
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


class QueryEntity(BaseModel):

    id = AutoField(db_column='query_id')
    name = CharField(db_column='query_name', unique=True, default='')
    query = TextField(db_column='query_sql', default='')

    class Meta:
        table_name = 'query'
