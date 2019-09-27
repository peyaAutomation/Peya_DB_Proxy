import os
from peewee import *

database = MySQLDatabase(
    os.environ['MY_SQL_DATABASE_QUERY_REPO'],
    **{
        'charset': 'utf8',
        'use_unicode': True,
        'host': os.environ['MY_SQL_HOST_QUERY_REPO'],
        'port': int(os.environ['MY_SQL_PORT_QUERY_REPO']),
        'user': os.environ['MY_SQL_USER_QUERY_REPO'],
        'password': os.environ['MY_SQL_PASS_QUERY_REPO']
    }
)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = None


class QueryEntity(BaseModel):
    id = AutoField(db_column='query_id')
    name = CharField(db_column='query_name', unique=True, default='')
    query = TextField(db_column='query_sql', default='')

    class Meta:
        table_name = 'query'
