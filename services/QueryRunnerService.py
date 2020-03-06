from mysql.connector import DatabaseError

from libs.MySQL_driver import MySQLDriver
from models.models import QueryEntity

my_sql_driver = MySQLDriver()


def run_query(query, alternative_result_mapping=False, data=None, database='peyadb'):
    my_sql_driver.connect(database)
    result = my_sql_driver.execute_query(query=query, alternative_result_mapping=alternative_result_mapping, data=data)
    my_sql_driver.close_connection()
    return result


def check_connection(database):
    try:
        my_sql_driver.connect(database)
        status = my_sql_driver.check_connection()
        my_sql_driver.close_connection()
    except DatabaseError:
        status = False

    return status


class QueryRunnerService:

    @staticmethod
    def run_query_by_name(query_name, alternative_result_mapping=False, database='peyadb'):
        query_dict = QueryEntity().select().where(QueryEntity.name == query_name).dicts().first()
        return run_query(query=query_dict['query'], alternative_result_mapping=alternative_result_mapping,
                         database=database)

    @staticmethod
    def run_custom_query(query, alternative_result_mapping=False, data='', database='peyadb'):
        return run_query(query=query, alternative_result_mapping=alternative_result_mapping, data=data,
                         database=database)

    @staticmethod
    def check_connection(database='peyadb'):
        return check_connection(database)